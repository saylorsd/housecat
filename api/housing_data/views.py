import logging
from typing import Union

from django.conf import settings
from django.contrib.gis.db.models.functions import Centroid
from django.db.models import QuerySet
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.decorators.csrf import csrf_exempt
from rest_framework import views, viewsets, filters
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response

from accounts.models import Watchlist
from housecat.content_negotiation import GeoJSONContentNegotiation
from housing_data.models import ProjectIndex
from housing_data.serializers import (
    ProjectIndexSerializer,
    ProjectIndexBriefSerializer,
    ProjectIndexGeoJSONSerializer, WatchlistSerializer, WatchlistDetailedSerializer,
)

logger = logging.getLogger(__name__)


def get_filtered_project_indices(request: Request) -> QuerySet[ProjectIndex]:
    queryset = ProjectIndex.objects \
        .annotate(centroid=Centroid('geom')) \
        .all()

    # Match filter form items from app's map page
    recent_sale = request.query_params.get('recent-sale')
    recent_foreclosure = request.query_params.get('recent-foreclosure')
    recent_code_violation = request.query_params.get('recent-code-violation')

    risk_level = request.query_params.get('risk-level')
    lihtc_compliance = request.query_params.get('lihtc-compliance')
    reac_score = request.query_params.get('reac-score')
    last_inspection = request.query_params.get('last-inspection')
    funding_category = request.query_params.get('funding-category')
    status = request.query_params.get('status')

    print(recent_sale)

    # run all the filters
    if recent_sale:
        queryset = ProjectIndex.filter_by_recent_sale(queryset, months=int(recent_sale))
    if recent_foreclosure:
        queryset = ProjectIndex.filter_by_recent_foreclosure(queryset, months=int(recent_foreclosure))
    if recent_code_violation:
        queryset = ProjectIndex.filter_by_recent_code_violation(queryset, months=int(recent_code_violation))

    if risk_level:
        queryset = ProjectIndex.filter_by_risk_level(queryset, lvl=risk_level)
    if lihtc_compliance:
        queryset = ProjectIndex.filter_by_lihtc_compliance(queryset, lvl=lihtc_compliance)
    if reac_score:
        queryset = ProjectIndex.filter_by_reac_score(queryset, lvl=reac_score)
    if last_inspection:
        queryset = ProjectIndex.filter_by_last_inspection(queryset, lvl=last_inspection)
    if funding_category:
        queryset = ProjectIndex.filter_by_funding_category(queryset, lvl=funding_category)
    if status:
        queryset = ProjectIndex.filter_by_status(queryset, val=status)
    return queryset


class WatchlistViewSet(viewsets.ModelViewSet):
    serializer_class = WatchlistSerializer
    queryset = Watchlist.objects.all()
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', ]
    lookup_field = 'slug'

    def get_serializer_class(self):
        if self.action == 'list':
            return WatchlistSerializer
        return WatchlistDetailedSerializer


class ProjectViewSet(viewsets.ModelViewSet):
    """
    Standard REST model viewset for Housing Projects.
    """
    filter_backends = [filters.SearchFilter, ]
    search_fields = ['hud_property_name', ]
    permission_classes = [IsAuthenticated]

    @csrf_exempt
    def list(self, request: Request, *args, **kwargs):
        return super(ProjectViewSet, self).list(self, request, *args, **kwargs)

    @csrf_exempt
    def retrieve(self, request: Request, *args, **kwargs):
        return super(ProjectViewSet, self).retrieve(self, request, *args, **kwargs)

    def get_serializer_class(self) -> type(Union[ProjectIndexSerializer, ProjectIndexBriefSerializer]):
        if self.action == 'list':
            return ProjectIndexBriefSerializer
        return ProjectIndexSerializer

    def get_queryset(self) -> QuerySet[ProjectIndex]:
        return get_filtered_project_indices(self.request)


class ProjectGeoJSONViewSet(viewsets.ModelViewSet):
    """
    Viewset that allows for GeoJSON file downloads and connections to third party mapping tools.
    """
    queryset = ProjectIndex.objects.all()
    serializer_class = ProjectIndexGeoJSONSerializer
    content_negotiation_class = GeoJSONContentNegotiation
    permission_classes = [IsAuthenticated]

    pagination_class = None

    def get_queryset(self) -> QuerySet[ProjectIndex]:
        return get_filtered_project_indices(self.request)


def kebab(string: str) -> str:
    return string.replace('_', '-').lower()


class ProjectVectorTileViewSet(views.APIView):
    """
    Provides necessary settings to render a mapbox-gl map plus additional settings for use with
      [@wprdc-widgets/map](https://github.com/WPRDC/frontend-libraries/tree/main/packages/%40wprdc-widgets/map)
      React component
    """
    permission_classes = [IsAuthenticated]

    def get_queryset(self) -> QuerySet[ProjectIndex]:
        return get_filtered_project_indices(self.request)

    @method_decorator(cache_page(settings.VIEW_CACHE_TTL))
    def get(self, request: Request) -> Response:
        # use complete set of projects, filtering will be handled by the layer's filter property
        logger.info(f'{request.user}|hey')

        map_view = settings.PUBLIC_HOUSING_PROJECT_LAYER_VIEW
        map_id = kebab(map_view)

        # base marker layer, can have filter added if need be
        circle_layer = {
            'id': f'{map_id}/marker',
            'source': map_id,
            'source-layer': f'maps.{map_view}',
            'type': 'circle',
            'paint': {
                'circle-opacity': 0.8,
                'circle-stroke-width': 1,
                'circle-radius': [
                    'step',
                    ['to-number', ['get', 'max_units']],
                    5,
                    50, 5,
                    100, 7.5,
                    250, 12.5,
                    500, 25,
                ],
                'circle-color': [
                    'match',
                    ['to-string', ['get', 'funding_category']],
                    'HUD Multifamily', '#7F3C8D',
                    'LIHTC', '#11A579',
                    'Public Housing', '#3969AC',
                    'HUD Multifamily|LIHTC', '#F2B701',
                    'LIHTC|Public Housing', '#F2B701',
                    'HUD Multifamily|LIHTC|Public Housing', '#F2B701',
                    'gray',
                ],
                'circle-stroke-color': [
                    'match',
                    ['to-string', ['get', 'status']],
                    'Closed', 'red',
                    'black'
                ]
            }
        }

        text_layer = {
            'id': f'{map_id}/text',
            'source': map_id,
            'source-layer': f'maps.{map_view}',
            'type': 'symbol',
            'layout': {
                'text-allow-overlap': True,
                'text-field': ['to-string', ['get', 'hud_property_name']],
                'text-offset': [0, 1],
                'text-anchor': 'top',
                'text-size': [
                    'interpolate',
                    ['linear'],
                    ['zoom'],
                    0, 0,
                    14, 0,
                    14.1, 12
                ]
            },
            'paint': {
                'text-opacity': [
                    "interpolate",
                    ["linear"],
                    ["zoom"],
                    0, 0,  # at zoom 0, have 0 opacity
                    14, 0,  # at zoom 14, have 0 but start to go up quickly
                    16, 1,
                    22, 1
                ]
            }
        }

        # only filter if necessary
        if len(self.request.query_params.keys()):
            # get set of id's to filter by
            projects = self.get_queryset()
            ids = [project.id for project in projects]
            # only those with an id in `ids`
            # https://docs.mapbox.com/mapbox-gl-js/style-spec/expressions
            circle_layer = {
                **circle_layer,
                'filter': ['in', ['get', 'id'], ['literal', ids]]
            }
            text_layer = {
                **text_layer,
                'filter': ['in', ['get', 'id'], ['literal', ids]]
            }
        return Response({
            'source': {
                'id': map_id,
                'type': 'vector',
                'url': f'{settings.MARTIN_PUBLIC_HOST}/maps.{map_view}.json'
            },
            'layers': [
                circle_layer,
                text_layer,
            ],
            'extras': {
                'legend_items': [
                    {
                        'key': 'hud-mf',
                        'variant': 'categorical',
                        'marker': '#7F3C8D',
                        'label': 'HUD Multifamily'
                    },
                    {
                        'key': 'lihtc',
                        'variant': 'categorical',
                        'marker': '#11A579',
                        'label': 'LIHTC'
                    },
                    {
                        'key': 'public-housing',
                        'variant': 'categorical',
                        'marker': '#3969AC',
                        'label': 'Public Housing'
                    },
                    {
                        'key': 'multiple',
                        'variant': 'categorical',
                        'marker': '#F2B701',
                        'label': 'More than one funding source'
                    },
                    {
                        'key': 'other',
                        'variant': 'categorical',
                        'marker': 'gray',
                        'label': 'Other/Unable to Determine'
                    },
                ]
            }
        })
