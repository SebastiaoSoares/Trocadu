import React from 'react';
import { IonButton } from '@ionic/react';

import styles from "./GameButton.module.css";

function Example() {
  return (
    <>
      <IonButton className={styles.gameButton}>Default</IonButton>
    </>
  );
}
export default Example;