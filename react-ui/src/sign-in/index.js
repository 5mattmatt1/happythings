import React, { useState } from 'react';
import Avatar from '@material-ui/core/Avatar';
import Button from '@material-ui/core/Button';
import CssBaseline from '@material-ui/core/CssBaseline';
import TextField from '@material-ui/core/TextField';
import FormControlLabel from '@material-ui/core/FormControlLabel';
import Checkbox from '@material-ui/core/Checkbox';
import Link from '@material-ui/core/Link';
import Grid from '@material-ui/core/Grid';
import Box from '@material-ui/core/Box';
import LockOutlinedIcon from '@material-ui/icons/LockOutlined';
import Typography from '@material-ui/core/Typography';
import { makeStyles } from '@material-ui/core/styles';
import Container from '@material-ui/core/Container';

function Copyright() {
  return (
    <Typography variant="body2" color="textSecondary" align="center">
      {'Copyright © '}
      <Link color="inherit" href="https://material-ui.com/">
        Happy Things
      </Link>{' '}
      {new Date().getFullYear()}
      {'.'}
    </Typography>
  );
}

// TODO: Might move this to a hooks directory
const useStyles = makeStyles((theme) => ({
  paper: {
    marginTop: theme.spacing(8),
    display: 'flex',
    flexDirection: 'column',
    alignItems: 'center',
  },
  avatar: {
    margin: theme.spacing(1),
    backgroundColor: theme.palette.secondary.main,
  },
  form: {
    width: '100%', // Fix IE 11 issue.
    marginTop: theme.spacing(1),
  },
  submit: {
    margin: theme.spacing(3, 0, 2),
  },
  invalid: {
      color: "0xCC2222"
  }
}));

export default function SignIn() {
  const classes = useStyles();
  const [invalidCredentials, setInvalidCredentials] = useState(false);
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');

  function validateForm()
  {
    console.log("validateForm");
    return username.length > 0 && password.length > 0;
  }

  function handleSubmit(event) 
  {
    let credentials = {
        username : username,
        password : password
    };

    fetch(`${process.env.REACT_APP_FLASK_BASE_URL}/api/auth/login`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(credentials)
        }
    ).then((response) => {
        console.log(response.status);
        if (response.status === 400)
        {
            console.log("Invalid credentials");
            setInvalidCredentials(true);
            return;
        }

        // Should get an access and refresh token
        return response.json();
    }).then((jwt_credentials) => {
      // Session storage isn't the most secure, but it'll do for this simple website.
      console.log(jwt_credentials);
      sessionStorage.setItem("jwt_access_token", jwt_credentials.login.access_token);
      sessionStorage.setItem("jwt_refresh_token", jwt_credentials.login.refresh_token);
      window.location.href = "/";
    }).catch((error) => {
        console.error('Error:', error);
    });
    event.preventDefault();
  }

  return (
    <Container component="main" maxWidth="xs">
      <CssBaseline />
      <div className={classes.paper}>
        <Avatar className={classes.avatar}>
          <LockOutlinedIcon />
        </Avatar>
        <Typography component="h1" variant="h5">
          Sign in
        </Typography>
        <form className={classes.form} onSubmit={handleSubmit}>
          <TextField
            variant="outlined"
            margin="normal"
            required
            fullWidth
            id="username"
            label="Username"
            name="username"
            onChange={evt => {setUsername(evt.target.value);}}
            autoComplete="username"
            autoFocus
          />
          <TextField
            variant="outlined"
            margin="normal"
            required
            fullWidth
            name="password"
            label="Password"
            type="password"
            id="password"
            onChange={evt => {setPassword(evt.target.value);}}
            autoComplete="current-password"
          />
          {invalidCredentials &&
            <Typography component="p" color="error">
                Invalid username or password
            </Typography>
          }
          <FormControlLabel
            control={<Checkbox value="remember" color="primary" />}
            label="Remember me"
          />
          <Button
            type="submit"
            fullWidth
            variant="contained"
            color="primary"
            disabled={!validateForm()}
            className={classes.submit}
          >
            Sign In
          </Button>
          {/* <Grid container>
            <Grid item xs>
              <Link href="#" variant="body2">
                Forgot password?
              </Link>
            </Grid>
            <Grid item>
              <Link href="#" variant="body2">
                {"Don't have an account? Sign Up"}
              </Link>
            </Grid>
          </Grid> */}
        </form>
      </div>
      <Box mt={8}>
        <Copyright />
      </Box>
    </Container>
  );
}
