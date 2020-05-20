import React, { useState } from 'react';
import Container from '@material-ui/core/Container';
import { Typography, Paper, Avatar, Divider, Grid } from '@material-ui/core';
import { Post } from './post';
import { makeStyles, Theme } from '@material-ui/core/styles';

const useStyles = makeStyles((theme: Theme) => ({
    root: {
        flexGrow: 1,
    },
    avatar: {
        align: 'center'
    },
    username: {
        textAlign: 'center',
        color: theme.palette.text.secondary,
    },
    bodyText: {
        color: theme.palette.text.primary,
    }
}));
  

export function PostComponent(props: any) {
    const classes = useStyles();
    let post: Post = props.post;
    console.log(post);
    console.log(post.text);
    
    return (
      <Container component="main" maxWidth="xs">
        <Paper>
            <Grid container spacing={3} justify="center">
                <Grid item xs={6}>
                    <Avatar 
                        className={classes.avatar}
                        src={`https://www.gravatar.com/avatar/${post.poster_email_hash}`}
                    >
                    </Avatar>
                </Grid>
                <Grid item xs={6}>
                    <Typography className={classes.username}>
                        {post.poster_username}
                    </Typography>
                </Grid>
                
                <Grid item xs={12}>
                    <Divider variant="middle" />
                </Grid>

                <Grid item xs={12}>
                    <Typography className={classes.bodyText}>
                        {post.text}
                    </Typography>
                </Grid>
            </Grid>
        </Paper>
      </Container>
    );
}
