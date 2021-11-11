import React, { Component } from "react";
import { 
    BrowserRouter as Router, 
    Switch, 
    Route, 
    Link, 
    Redirect 
} from "react-router-dom"
import { 
    TextField, 
    Button, 
    Grid, 
    Typography 
} from "@material-ui/core";

import RoomJoinPage from "./RoomJoinPage";
import RoomCreatePage from "./RoomCreatePage";
import Room from "./Room";


export default class HomePage extends Component{
    constructor(props){
        super(props);
    }

    render() {
        return (
            <Router>
                <Switch>
                    <Route exact path="/">
                        <Grid container spacing={1}>
                            <Grid item xs={12} align="center">
                                <Typography variant="h4" component="h4">
                                    <p>Welcom Home</p>
                                </Typography>
                            </Grid>
                            <Grid item xs={12} align="center">
                                <Button 
                                    variant="contained"
                                    color="secondary"
                                    href="/create"
                                >
                                    Create New Room!
                                </Button>
                            </Grid>
                            <Grid item xs={12} align="center">
                                <Button 
                                    variant="contained"
                                    color="primary"
                                    href="/join"
                                >
                                    Join Room
                                </Button>
                            </Grid>
                        </Grid>
                    </Route>
                    <Route path="/join" component={RoomJoinPage} />
                    <Route path="/create" component={RoomCreatePage} />
                    <Route path="/room/:roomCode" component={Room} />
                </Switch>
            </Router>
        );
    }
}
    