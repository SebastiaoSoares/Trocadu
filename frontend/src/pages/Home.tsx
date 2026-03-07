import { IonContent, IonHeader, IonPage, IonTitle, IonToolbar } from '@ionic/react';

import { Background } from '../components/';

import styles from "./Home.module.css"
import logo from '../assets/images/trocadu.png';

const Home: React.FC = () => {
  return (
    <IonPage>
      <Background />
      <IonHeader>
        <IonToolbar className={styles.toolbar}>
          <IonTitle>
            <img src={logo} alt="Trocadu Icon" height="50" />
          </IonTitle>
        </IonToolbar>
      </IonHeader>
      <IonContent fullscreen>
        <IonHeader collapse="condense">
          <IonToolbar>
            <IonTitle size="large">Trocadu</IonTitle>
          </IonToolbar>
        </IonHeader>
      </IonContent>
    </IonPage>
  );
};

export default Home;
