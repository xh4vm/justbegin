import React from 'react';
import { Slider } from '../Slider';
import styles from './ContentBlock.module.css';

const myArr = ["/images/slide_cat.jpg", "/images/slide_sea.jpg", "/images/slide_home.png", "/images/slide_somthing.png", "/images/image 3.png", "/images/image 4.jpg", "/images/image 5.png"]

export const ContentBlock = () => {
    return (
        <>
            <div className={styles.wrapper}>
                <Slider arr={myArr}></Slider>
            </div>
                <div className={styles.ContentBlock}>
                    <div className={styles.sphire} style={{backgroundImage: "url(/images/DesktopBest.png)"}}>
                        <div className={styles.registrateWrapper}>
                            <div className={styles.createrWrapper}>
                                <div className={styles.createrWrapperDescription}>
                                    <ul className={styles.createrWrapperList}>
                                    <li className={styles.createrWrapperName}>
                                        CREATORS
                                    </li>
                                        <li className={styles.createrWrapperListItem}>Find one mind</li>
                                        <li className={styles.createrWrapperListItem}>Get answers to your<br></br>questions in the group chat</li>
                                        <li className={styles.createrWrapperListItem}>Share your experience with beginners</li>
                                        <li className={styles.createrWrapperListItem}>Create your project and get investment</li>
                                    </ul>
                                </div>
                                <div className={styles.createrWrapperRegistrate}>
                                    <div><img src="/images/Ellipse.png" alt="ellipse" width="260px" height="260px"></img></div>
                                    <a href="#" className={styles.createrWrapperRegistrateLink}>REGISTRATE</a>
                                </div>
                            </div>
                            <div className={styles.investrWrapper}>
                                <div className={styles.investrWrapperRegistrate}></div>
                                <div className={styles.investrWrapperDescription}>
                                        <ul className={styles.investrWrapperList}>
                                            <li className={styles.investrWrapperName}>
                                                Investors           
                                            </li>
                                            <li className={styles.investrWrapperListItem}>Invest in attractive and profitable projects</li>
                                            <li className={styles.investrWrapperListItem}>Get direct contact with developers</li>
                                            <li className={styles.investrWrapperListItem}>Become an integral part of the project</li>
                                        </ul>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
        </>
    )
}