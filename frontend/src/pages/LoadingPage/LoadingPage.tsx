import { useEffect } from 'react';
import { useIonRouter } from '@ionic/react';

import { GameContent, GamePage } from '../../components';

import styles from "./LoadingPage.module.css";
import logo from '../../assets/images/trocadu.png';

const LoadingPage: React.FC = () => {
  const router = useIonRouter();

  useEffect(() => {
    const timer = setTimeout(() => {
      
      router.push('/home', 'back', 'push');
      
    }, 3000);

    return () => clearTimeout(timer);
  }, [router]);

  return (
    <GamePage>
      <GameContent fullscreen>
        <div className={styles.menuContainer}>
          <img src={logo} alt="Trocadu Icon" className={styles.logo} />
        </div>
      </GameContent>
    </GamePage>
  );
};

export default LoadingPage;
