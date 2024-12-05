import React, { useState } from 'react';
import { Box, Button, FormControl, FormLabel, Input, VStack, useToast, Icon, Flex, useBreakpointValue } from '@chakra-ui/react';
import { FaFacebook } from 'react-icons/fa';
import axios from 'axios';
import FacebookLogin from 'react-facebook-login';

interface LoginProps {
  onLogin: (username: string, userId: string) => void;
  onLoginWithGoogle: () => void;
  onLoginWithFacebook: () => void;
}

interface ReactFacebookLoginInfo {
  accessToken: string;
  userID: string;
  expiresIn: number;
  signedRequest: string;
  email?: string;
  name?: string;
  picture?: {
    data: {
      height: number;
      is_silhouette: boolean;
      url: string;
      width: number;
    };
  };
}

interface ReactFacebookFailureResponse {
  status?: string;
}

const LoginForm: React.FC<LoginProps> = ({ onLogin, onLoginWithGoogle, onLoginWithFacebook }) => {
  const [username, setUsername] = useState<string>('');
  const [password, setPassword] = useState<string>('');
  const toast = useToast();
  const apiUrl = 'http://localhost:5000';

  const handleLogin = async () => {
    try {
      const response = await axios.post(`${apiUrl}/auth/login`, { username, password });
      localStorage.setItem('jwt', response.data.access_token);
      onLogin(username, response.data.user_id);
      toast({
        title: 'Connexion réussie',
        description: 'Vous êtes maintenant connecté.',
        status: 'success',
        duration: 9000,
        isClosable: true,
      });
    } catch (error) {
      toast({
        title: 'Échec de la connexion',
        description: error.response?.data?.message,
        status: 'error',
        duration: 9000,
        isClosable: true,
      });
    }
  };

  const handleFacebookLogin = (response: ReactFacebookLoginInfo | ReactFacebookFailureResponse) => {
    console.log('Facebook login response:', response);
    if ('accessToken' in response) {
      axios.post(`${apiUrl}/auth/facebook_login`, {
        accessToken: response.accessToken
      }).then(res => {
        localStorage.setItem('jwt', res.data.access_token);
        onLogin(response.name || 'Default Username', res.data.user_id);
        toast({
          title: 'Connexion Facebook réussie',
          description: 'Vous êtes maintenant connecté avec Facebook.',
          status: 'success',
          duration: 9000,
          isClosable: true,
        });
      }).catch(error => {
        toast({
          title: 'Échec de la connexion Facebook',
          description: 'La connexion a échoué. Veuillez réessayer.',
          status: 'error',
          duration: 9000,
          isClosable: true,
        });
      });
    } else {
      toast({
        title: 'Échec de la connexion Facebook',
        description: 'Facebook login failed. Please try again.',
        status: 'error',
        duration: 9000,
        isClosable: true,
      });
    }
  };

  return (
    <Flex align="center" justify="center" height="100vh">
      <Box width={useBreakpointValue({ base: "90%", md: "400px" })} rounded="lg" bg="white" boxShadow="lg" p={8}>
        <VStack spacing={4}>
          <FormControl isRequired>
            <FormLabel>Nom d'utilisateur</FormLabel>
            <Input value={username} onChange={(e) => setUsername(e.target.value)} placeholder="Nom d'utilisateur"/>
          </FormControl>
          <FormControl isRequired mt={4}>
            <FormLabel>Mot de passe</FormLabel>
            <Input type="password" value={password} onChange={(e) => setPassword(e.target.value)} placeholder="Mot de passe"/>
          </FormControl>
          <Button mt={4} colorScheme="blue" onClick={handleLogin}>Se connecter</Button>
          <FacebookLogin
            appId="1554210685119210"
            autoLoad={false}
            fields="name,email,picture"
            callback={handleFacebookLogin}
            render={({ onClick }) => (
              <Button leftIcon={<Icon as={FaFacebook} />} mt={4} colorScheme="facebook" onClick={onClick}>
                Se connecter avec Facebook
              </Button>
            )}
          />
        </VStack>
      </Box>
    </Flex>
  );
};

export default LoginForm;