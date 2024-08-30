import { createTheme } from '@mui/material/styles';

// Define the color palette
const theme = createTheme({
  palette: {
    primary: {
      main: '#FFFFFF', // White for primary color
    },
    secondary: {
      main: '#005776', // Solid Blue for secondary color
    },
    background: {
      default: '#192B37', // Dark background color
      paper: '#192B37', // Dark paper background color
    },
    text: {
      primary: '#FFFFFF', // White text color for primary
      secondary: '#FFFFFF', // White text color for secondary
    },
  },
  typography: {
    fontFamily: 'DavaSans, Roboto, sans-serif',
  },
  components: {
    MuiButton: {
      styleOverrides: {
        root: {
          borderRadius: '50px', // Rounds the buttons
          border: '2px solid white', // White outline
          textTransform: 'none', // Prevents all caps text
        },
        outlined: {
          borderColor: 'white', // Ensures outlined buttons have a white border
        },
      },
    },
  },
});

export default theme;
