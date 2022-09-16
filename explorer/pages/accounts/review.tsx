import styles from '../../styles/Accounts.module.css';
import { useAccountList } from '@wprdc-connections/housecat';

export function AccountReviewPage() {
  const { data: userList, error } = useAccountList();

  return (
    <div className={styles.wrapper}>
      {userList?.map((user) => (
        <pre key={user.affiliation}>{JSON.stringify(user, null, 2)}</pre>
      ))}
    </div>
  );
}

export default AccountReviewPage;
