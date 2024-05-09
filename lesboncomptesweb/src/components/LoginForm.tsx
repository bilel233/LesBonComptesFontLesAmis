import React, { useState } from 'react';
import axios from 'axios';
import {
  Box, Button, FormControl, FormLabel, Input, Stack, useColorModeValue, useToast, Icon
} from '@chakra-ui/react';
import { FcGoogle } from 'react-icons/fc';
import { FaFacebook } from 'react-icons/fa';

interface LoginProps {
  onLogin: (username: string, password: string) => void;
  onLoginWithGoogle: () => void;
  onLoginWithFacebook: () => void;
}

const LoginForm: React.FC<LoginProps> = ({ onLoginWithGoogle }) => {
  const [username, setUsername] = useState<string>('');
  const [password, setPassword] = useState<string>('');
  const toast = useToast();
  const apiUrl = 'http://localhost:5000';  // Assurez-vous que cela correspond à l'URL de votre serveur Flask

  const handleLogin = async () => {
    try {
      const response = await axios.post(`${apiUrl}/auth/login`, { username, password });
      toast({
        title: 'Login Successful',
        description: response.data.access_token,
        status: 'success',
        duration: 9000,
        isClosable: true,
      });

    } catch (error) {
      toast({
        title: 'Login Failed',
        description: error.response?.data?.message,
        status: 'error',
        duration: 9000,
        isClosable: true,
      });
    }
  };

  const handleFacebookLogin = () => {

    window.location.href = `${apiUrl}/auth/facebook_login`;
  };

  return (
    <Box rounded={'lg'} bg={useColorModeValue('white', 'gray.700')} boxShadow={'lg'} p={8}>
      <Stack spacing={4}>
        <FormControl isRequired>
          <FormLabel>Username</FormLabel>
          <Input type="text" value={username} onChange={(e) => setUsername(e.target.value)} />
        </FormControl>
        <FormControl isRequired mt={6}>
          <FormLabel>Password</FormLabel>
          <Input type="password" value={password} onChange={(e) => setPassword(e.target.value)} />
        </FormControl>
        <Button type="button" width="full" mt={4} colorScheme="telegram" onClick={handleLogin}>
          Log in
        </Button>
        <Button leftIcon={<Icon as={FcGoogle} />} width="full" mt={2} onClick={onLoginWithGoogle}>
          Login with Google
        </Button>
        <Button leftIcon={<Icon as={FaFacebook} />} width="full" mt={2} colorScheme="facebook" onClick={handleFacebookLogin}>
          Login with Facebook
        </Button>
      </Stack>
    </Box>
  );
};

export default LoginForm;
