import { Redirect, Route } from 'react-router-dom';
import { IonApp, IonRouterOutlet, setupIonicReact } from '@ionic/react';
import { IonReactRouter } from '@ionic/react-router';

import { Background } from './components/';

import { ConfigMode, Configurations, Home, LoadingPage, PlayGame, SelectMode } from './pages/';

import '@ionic/react/css/core.css';
import '@ionic/react/css/normalize.css';
import '@ionic/react/css/structure.css';
import '@ionic/react/css/typography.css';
import '@ionic/react/css/padding.css';
import '@ionic/react/css/float-elements.css';
import '@ionic/react/css/text-alignment.css';
import '@ionic/react/css/text-transformation.css';
import '@ionic/react/css/flex-utils.css';
import '@ionic/react/css/display.css';
import '@ionic/react/css/palettes/dark.system.css';

import './theme/variables.css';

setupIonicReact();

const App: React.FC = () => (
  <IonApp>
    <Background />

    <IonReactRouter>
      <IonRouterOutlet>

        <Route exact path="/loading">
          <LoadingPage />
        </Route>

        <Route exact path="/home">
          <Home />
        </Route>

        <Route exact path="/">
          <Redirect to="/loading" />
        </Route>

        <Route exact path="/config-mode">
          <ConfigMode />
        </Route>

        <Route exact path="/configurations">
          <Configurations />
        </Route>

        <Route exact path="/play-game">
          <PlayGame />
        </Route>

        <Route exact path="/select-mode">
          <SelectMode />
        </Route>

      </IonRouterOutlet>
    </IonReactRouter>
  </IonApp>
);

export default App;
