import React from 'react';
import { Link } from 'react-router-dom';
import styles from './Autorization.module.css'

export const Autorization = () => {
    return (
        <>
            <div className={styles.autorizationPage} style={{backgroundImage: "url(/images/DesktopBest.png)"}} >
                <div className={styles.autorizationWrapper}>
                    <div className={styles.contentWrapper}>
                        <div className={styles.helperClass}>
                            <form className={styles.myForm}>
                                <div className={styles.myFormInputBlock}>
                                    <strong className={styles.myFormInputLabel}>Login:</strong>
                                    <input className={styles.myFormInput} type="text"></input>
                                </div>
                                <div className={styles.myFormInputBlock}>
                                    <strong className={styles.myFormInputLabel}>Password:</strong>
                                    <input className={styles.myFormInput} type="password"></input>
                                </div>
                                <div className={styles.secondHelp}>
                                    <button type='submit' className={styles.subButtin}>Enter</button>
                                    <span className={styles.myLink}>Я забыл свои данные...</span>
                                </div>
                            </form>
                        </div>
                        <div className={styles.helperClass}><div className={styles.pickLink}><Link to="/"><img src="/images/svgBebeshka.svg" alt="bebesha here" className={styles.logoForDisign}></img></Link></div></div>
                    </div>
                </div>
            </div>
        </>
    )
}