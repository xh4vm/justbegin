import React, { useEffect} from 'react';
import styles from './AutorizationBlock.module.css'
import styles2 from '../Header/Header.module.css'
import { Link } from 'react-router-dom'


export const AutorizationBlock = () => {
    useEffect(() => {
        window.addEventListener("keydown", function(evt){
            if (evt.keyCode === 27){
              if (document.querySelector('#modal').classList.contains(`${styles2.activeModal}`)){
                evt.preventDefault();
                document.querySelector('#modal').classList.remove(`${styles2.activeModal}`)
                document.querySelector('#MyAutorizationWrapper').classList.remove(`${styles2.MyAutorizationWrapper}`)
              }
            }
         })
    }, []
    )
    const quit = () => {
        document.querySelector('#modal').classList.remove(`${styles2.activeModal}`)
        document.querySelector('#MyAutorizationWrapper').classList.remove(`${styles2.MyAutorizationWrapper}`)
    }
    const quit2 = (e) => {
        if (e.target.id === 'helper') {
            document.querySelector('#modal').classList.remove(`${styles2.activeModal}`)
            document.querySelector('#MyAutorizationWrapper').classList.remove(`${styles2.MyAutorizationWrapper}`)
        }
    }
    return (
        <>
        <div className={styles.helper} onClick={quit2} id={'helper'}>
            <div className={styles.autorizationWrapper} id={'MyAutorizationWrapper'}>
                <h2 className={styles.title}>Autorization</h2> 
                <form>
                    <div className={styles.inputBox}>
                        <input type='text' className={styles.inputBoxInput} required='required'></input>
                        <span className={styles.inputBoxInputLabel}>Login:</span>
                    </div>
                    <div className={styles.inputBox}>
                        <input type='password' className={styles.inputBoxInput} required='required'></input>
                        <span className={styles.inputBoxInputLabel}>Password:</span>
                    </div>
                    <div className={styles.inputBox}>
                        <button onClick={quit}>Subscrube</button>
                    </div>
                </form>  
                <Link to={"/biba"} className={styles.regLink}><span>Registration</span></Link>     
            </div>
        </div>
        </>
    )
}