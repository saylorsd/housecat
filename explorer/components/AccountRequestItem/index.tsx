import styles from './AccountRequestItem.module.css';
import { UserProfile } from '@wprdc-types/housecat';
import { Button } from '@wprdc-components/button';

export interface AccountRequestItemProps {
  userProfile: UserProfile;
  onDeny: (profile: UserProfile) => void;
  onApprove: (profile: UserProfile) => void;
}

export function AccountRequestItem(props: AccountRequestItemProps) {
  const { userProfile, onApprove, onDeny } = props;
  const {
    id,
    affiliation,
    category,
    user,
    approved,
    agreedToTerms,
    expirationDate,
    ...fields
  } = userProfile;

  return (
    <div className={styles.wrapper}>
      <div>
        <h3>{user.email}</h3>
        <div className={styles.timestamp}>
          <span>Requested on: </span>
          <span>{new Date(user.dateJoined).toLocaleDateString()}</span>
        </div>
        <p className={styles.category}>{category}</p>{' '}
        <p className={styles.affiliation}>{affiliation}</p>
        <dl>
          {Object.entries(fields).map(([field, value]) => (
            <div key={field}>
              <dt>{toTitleCase(field)}</dt>
              <dd>{value}</dd>
            </div>
          ))}
        </dl>
      </div>
      <div className={styles.actions}>
        <div></div>
        <div className={styles.buttons}>
          <Button
            className={styles.approve}
            onPress={() => onApprove(userProfile)}
          >
            Approve
          </Button>
          <Button className={styles.deny} onPress={() => onDeny(userProfile)}>
            Deny
          </Button>
        </div>
      </div>
    </div>
  );
}

function toTitleCase(str: string): string {
  const temp = str.replace(/([A-Z])/g, ' $1');
  return temp.charAt(0).toUpperCase() + temp.slice(1);
}
