import { createMuiTheme } from '@material-ui/core/styles';
import purple from '@material-ui/core/colors/purple';
import green from '@material-ui/core/colors/green';
import blue from '@material-ui/core/colors/blue';
import red from '@material-ui/core/colors/red';

export const lightTheme = createMuiTheme({
    palette: {
        type: 'light',
    },
});

export const darkTheme = createMuiTheme({
    palette: {
        type: 'dark',
    },
});

export default lightTheme;