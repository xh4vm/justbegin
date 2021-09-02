import React from 'react';
import { AutorizationBlock } from '../../components';
import styles from './Autorization.module.css'

export const Autorization = () => {
    return (
        <>
            <div className={styles.autorizationPage} style={{backgroundImage: "url(/images/DesktopBest.png)"}} >
                <AutorizationBlock></AutorizationBlock>
            </div>
        </>
    )
}