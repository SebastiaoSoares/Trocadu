import { IonContent, IonHeader, IonPage, IonTitle, IonToolbar } from '@ionic/react';

import { Background } from '../../components';

import logo from '../assets/images/trocadu.png';

const LoadingPage: React.FC = () => {
  return (
    <IonPage>
      <IonContent fullscreen>
        <Background />
        <IonHeader collapse="condense">
          <IonToolbar>
            <IonTitle size="large">
                <img src={logo} alt="Trocadu Icon" height="50" />
            </IonTitle>
          </IonToolbar>
        </IonHeader>
      </IonContent>
    </IonPage>
  );
};

export default LoadingPage;
