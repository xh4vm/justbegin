import React, { useEffect } from 'react';
import styles from './WelcomeBanner.module.css'

export const WelcomeBanner = () => {
    
    return (
        <>
            <div className={styles.bannerWrapper} style={{backgroundImage: "url(/images/background1.png)"}}>
                <div className={styles.welcomTitleWrapper}>
                    <hr className={styles.titleBorder}></hr>
                        <div className={styles.title}>
                            <h5>MAKE YOUR DREAM COME TRUE OR INVEST IN PROJECTS CHANGING THE FUTURE</h5>
                        </div>
                    <hr className={styles.titleBorder}></hr>
                </div>
            </div>
        </>
    )
}