import React from 'react';
import {Header} from '../../components/Header/Header';
import { WelcomeBanner } from '../../components/Banners/WelcomeBanner';
import { AutorizationBlock, ContentBlock, Footer, NavigationPanel } from '../../components';
import styles from './WelcomePage.module.css'

const myArr = ['Arts','Comics & ilustration', 'Design & Tech', 'Film', 'Food & Craft', 'Games', 'Music', 'Publishing']

export const WelcomePage = () => {
    return(
        <div className="App">
            <Header></Header>
             <WelcomeBanner></WelcomeBanner>
             <NavigationPanel arr={myArr}></NavigationPanel>
             <ContentBlock></ContentBlock>
             <Footer></Footer>
             <div className={styles.AutorizationModal} id={'modal'}>
                <AutorizationBlock></AutorizationBlock>
             </div>
        </div>
    )
}
