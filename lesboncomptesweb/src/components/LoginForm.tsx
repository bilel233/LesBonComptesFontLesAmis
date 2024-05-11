
import React, { useState } from 'react';
import {
  Box, Button, FormControl, FormLabel, Input, Stack, useColorModeValue, useToast, Icon,
  Flex, useBreakpointValue
} from '@chakra-ui/react';
import { FcGoogle } from 'react-icons/fc';
import { FaFacebook } from 'react-icons/fa';
import axios from "axios";

interface LoginProps {
  onLogin: (username: string) => void;
  onLoginWithGoogle: () => void;
  onLoginWithFacebook: () => void;
}

const LoginForm: React.FC<LoginProps> = ({ onLogin, onLoginWithGoogle, onLoginWithFacebook }) => {
  const [username, setUsername] = useState<string>('');
  const [password, setPassword] = useState<string>('');
  const toast = useToast();
  const apiUrl = 'http://localhost:5000';

 const handleLogin = async () => {
  try {
    const response = await axios.post(`${apiUrl}/auth/login`, { username, password });
    toast({
      title: 'Login Successful',
      description: 'You are now logged in.',
      status: 'success',
      duration: 9000,
      isClosable: true,
    });
    localStorage.setItem('jwt', response.data.access_token);
    onLogin(username);
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


  return (
    <Flex align="center" justify="center" height="100vh">
      <Box width={useBreakpointValue({ base: "90%", md: "400px" })} rounded="lg" bg={useColorModeValue('white', 'gray.700')} boxShadow="lg" p={8}>
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
          <Button leftIcon={<Icon as={FaFacebook} />} width="full" mt={2} colorScheme="facebook" onClick={onLoginWithFacebook}>
            Login with Facebook
          </Button>
        </Stack>
      </Box>
    </Flex>
  );
};

export default LoginForm;
