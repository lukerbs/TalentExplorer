// Import React and Material-UI components
"use client";

import React, { useState } from 'react';
import {
  Container,
  TextField,
  Button,
  Typography,
  Box,
  Card,
  CardContent,
  CardMedia,
  Grid,
  Accordion,
  AccordionDetails,
  CircularProgress
} from '@mui/material';
import axios from 'axios';

// Define the Resume interface for TypeScript
interface Resume {
  id: number;
  name: string;
  photo: string;
  resume: string;
  qualifications?: string[];
  explanation?: string; // Store explanation text
  similarity: number;
  explanationOpen?: boolean;
  loading?: boolean;
}

// The Home functional component
const Home = () => {
  // State hooks for job description, results, and error handling
  const [jobDescription, setJobDescription] = useState<string>('');
  const [results, setResults] = useState<Resume[]>([]);
  const [error, setError] = useState<string | null>(null);

  // Handler for the search operation
  const handleSearch = async () => {
    try {
      const response = await axios.post('http://127.0.0.1:5000/api/search', { job_description: jobDescription });
      setResults(response.data);
      setError(null);
    } catch (err) {
      setError('Failed to fetch search results. Please try again later.');
      console.error(err);
    }
  };

  // Handler for explaining qualifications and explanations based on an ID
  const handleExplain = async (id: number) => {
    setResults(results.map(result => {
      if (result.id === id) {
        return { ...result, loading: true };
      }
      return result;
    }));

    try {
      const response = await axios.post('http://127.0.0.1:5000/api/explain', { id, job_description: jobDescription });
      const { qualifications, explanation } = response.data;
      const updatedResults = results.map(result => {
        if (result.id === id) {
          return { ...result, qualifications, explanation, explanationOpen: true, loading: false };
        }
        return result;
      });
      setResults(updatedResults);
      setError(null);
    } catch (err) {
      setError('Failed to fetch explanation. Please try again later.');
      console.error(err);
    }
  };

  // Handler to toggle the explanation view
  const toggleExplanation = (id: number) => {
    setResults(results.map(result => {
      if (result.id === id) {
        return { ...result, explanationOpen: !result.explanationOpen };
      }
      return result;
    }));
  };

  // Render the component
  return (
    <Container>
      <Box my={4}>
        <Box display="flex" alignItems="center">
          <Typography variant="h4" gutterBottom color="primary">
            <strong>endava</strong> <Box component="img" src="/Endava_Symbol.svg" alt="Custom Icon" sx={{ height: '.6em', marginRight: 1 }} />
          </Typography>
        </Box>
        <TextField
          className="custom-textfield"
          label="Job Description"
          multiline
          rows={4}
          variant="outlined"
          fullWidth
          value={jobDescription}
          onChange={(e) => setJobDescription(e.target.value)}
          InputProps={{
            sx: {
              borderRadius: '16px',
              overflow: 'auto',
            },
          }}
          sx={{ borderRadius: 2 }}
        />
        <Box my={2}>
          <Button
            variant="outlined"
            color="primary"
            onClick={handleSearch}
            sx={{
              color: 'white',
              borderWidth: '2px',
              '&:hover': {
                borderWidth: '2px',
              },
            }}
          >
            <Box display="flex" alignItems="center">
              Search
              <Box component="span" sx={{ display: 'flex', alignItems: 'center', marginLeft: 1 }}>
                <svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                  <path d="M5 11.0002L19.586 11.0002L15.2929 6.70711C14.9024 6.31658 14.9024 5.68342 15.2929 5.29289C15.6834 4.90237 16.3166 4.90237 16.7071 5.29289L22.7071 11.2929C22.8225 11.4083 22.9038 11.5449 22.951 11.6902C22.9808 11.7818 22.997 11.8768 22.9996 11.9722C22.9996 11.9732 22.9997 11.9742 22.9997 11.9751C22.9999 11.9822 23 11.9893 23 11.9964C23 11.9976 23 11.9989 23 12.0001C23 12.2821 22.8833 12.5369 22.6955 12.7187L16.7071 18.7071C16.3166 19.0976 15.6834 19.0976 15.2929 18.7071C14.9024 18.3166 14.9024 17.6834 15.2929 17.2929L19.5856 13.0002L5 13.0002L4.99668 13.0002C4.72171 12.9993 4.47299 12.8875 4.29271 12.7072L3.89655 12.307C3.78702 12.1975 3.64344 12.143 3.49987 12.1433C3.35629 12.143 3.21272 12.1975 3.10318 12.307L2.70703 12.7072C2.52606 12.8882 2.27613 13.0002 1.99991 13.0002C1.44766 13.0002 1 12.5525 1 12.0003C1 11.448 1.44766 11.0004 1.99991 11.0004C2.27613 11.0004 2.52606 11.1122 2.70703 11.2932L3.10318 11.6934C3.21272 11.8029 3.35629 11.8574 3.49987 11.857C3.64344 11.8574 3.78702 11.8029 3.89655 11.6934L4.29271 11.2932C4.3613 11.2246 4.43981 11.1659 4.5259 11.1195C4.66699 11.0434 4.82845 11.0002 5 11.0002Z" fill="white"/>
                </svg>
              </Box>
            </Box>
          </Button>
        </Box>
        <Box my={4} /> {/* Add additional spacing */}
        {error && (
          <Typography color="error" variant="body2">
            {error}
          </Typography>
        )}
        <Grid container spacing={2}>
          {results.map(result => (
            <Grid item xs={12} key={result.id}>
              <Card sx={{ border: '2px solid #5E6A73', borderRadius: '16px', position: 'relative' }}>
                <Grid container spacing={2}>
                  <Grid item xs={4}>
                    <CardMedia
                      component="img"
                      height="140"
                      image={`/photos/${result.photo}`}
                      alt={`Photo of ${result.name}`}
                      sx={{ borderRadius: '16px 0 0 16px' }} // Rounded corners for the image
                    />
                  </Grid>
                  <Grid item xs={8}>
                    <CardContent>
                      <Typography variant="h5" color="primary"><strong>{result.name}</strong></Typography>
                      <Typography variant="body1" color="textPrimary">{result.resume}</Typography>
                      <Box my={.8} /> 
                      <Button
                        variant="outlined"
                        color="primary"
                        onClick={() => result.qualifications ? toggleExplanation(result.id) : handleExplain(result.id)}
                        sx={{
                          borderWidth: '2px', // Ensures border width remains the same on hover
                          '&:hover': {
                            borderWidth: '2px',
                          },
                        }}
                        disabled={result.loading} // Disable button while loading
                      >
                        <Typography component="span" sx={{ color: result.loading ? '#5E6A73' : 'inherit' }}>
                          {result.loading ? 'Loading...' : result.explanationOpen ? 'Hide Explanation' : 'Explain'}
                        </Typography>
                        <Box component="span" sx={{ display: 'flex', alignItems: 'center', marginLeft: 1 }}>
                          {result.loading ? (
                            <CircularProgress size={24} sx={{ color: 'white' }} /> // Show spinner while loading
                          ) : (
                            <Box
                              component="img"
                              src={result.explanationOpen ? "/chevron-up.svg" : "/arrow-right.svg"}
                              alt={result.explanationOpen ? "Chevron Up Icon" : "Arrow Right Icon"}
                              sx={{ width: 24, height: 24 }}
                            />
                          )}
                        </Box>
                      </Button>
                    </CardContent>
                  </Grid>
                  {result.qualifications && result.explanationOpen && (
                    <Grid item xs={12}>
                      <Accordion expanded={result.explanationOpen}>
                        <AccordionDetails>
                          <Typography variant="body2" color="textSecondary"><strong>Qualifications:</strong></Typography>
                          <Grid container spacing={0}>
                            {result.qualifications.map((qualification, index) => (
                              <Grid item xs={4} key={index}>  {/* Changed from xs={12} to xs={4} */}
                                <Box display="flex" alignItems="center" my={1}>
                                  <Box component="img" src="/checkmark.svg" alt="Check Icon" sx={{ width: 24, height: 24, marginRight: 1 }} />
                                  <Typography>{qualification}</Typography>
                                </Box>
                              </Grid>
                            ))}
                          </Grid>
                          <Box mt={2}>
                            <Typography variant="body2" color="textSecondary"><strong>Explanation:</strong></Typography>
                            <Typography>{result.explanation}</Typography>
                          </Box>
                        </AccordionDetails>
                      </Accordion>
                    </Grid>
                  )}
                </Grid>
                <Box position="absolute" top={16} right={16} display="flex" alignItems="center" justifyContent="center">
                  <Box position="relative" display="flex" alignItems="center" justifyContent="center" width={60} height={60}>
                    <CircularProgress
                      variant="determinate"
                      value={result.similarity * 100}
                      size={60}
                      thickness={4}
                      sx={{ color: result.similarity >= 0.7 ? '#3DD17B' : '#FF5640' }} // Conditional color
                    />
                    <Box
                      top={0}
                      left={0}
                      bottom={0}
                      right={0}
                      position="absolute"
                      display="flex"
                      alignItems="center"
                      justifyContent="center"
                    >
                      <Typography variant="caption" component="div" color="textSecondary">
                        {Math.round(result.similarity * 100)}%
                      </Typography>
                    </Box>
                  </Box>
                </Box>
              </Card>
            </Grid>
          ))}
        </Grid>
      </Box>
    </Container>
  );
};

export default Home;
