import React from 'react';
import logo from './logo.svg';
import './App.css';

import { Button } from '@material-ui/core';
import Home from './home';
import SignIn from './sign-in';
import dotenv from 'dotenv';

import { BrowserRouter, Switch } from 'react-router-dom';
import { GuardProvider, GuardedRoute } from 'react-router-guards';

function App() {
  // let result = dotenv.config();
  
  // if (result.error)
  // {
  //   throw result.error;
  // }

  const requireLogin = (to: any, from: any, next: any) => {
    if (to.meta.auth) {
      let logged_in: boolean = true;
      logged_in = logged_in && sessionStorage.getItem("jwt_access_token") !== null;
      logged_in = logged_in && sessionStorage.getItem("jwt_refresh_token") !== null;

      if (logged_in) {
        next();
      }

      next.redirect('/login');
    } else {
      next();
    }
  };

  return (
    <div className="App">   
      <BrowserRouter>   
        {
          // loading={Loading} error={NotFound}
        }
        <GuardProvider guards={[requireLogin]}>
          <Switch>
            <GuardedRoute path="/login" exact component={SignIn} />
            <GuardedRoute path="/" exact component={Home} meta={{ auth: true }} />
          </Switch>
        </GuardProvider>
      </BrowserRouter>
      {/* <header className="App-header">
        <img src={logo} className="App-logo" alt="logo" />
        <Button color="primary">Hello World</Button>
        <p>
          Edit <code>src/App.tsx</code> and save to reload.
        </p>
        <a
          className="App-link"
          href="https://reactjs.org"
          target="_blank"
          rel="noopener noreferrer"
        >
          Learn React
        </a>
      </header> */}
    </div>
  );
}

export default App;
