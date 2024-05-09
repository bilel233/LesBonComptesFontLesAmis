import * as React from 'react';
import { ChakraProvider } from '@chakra-ui/react';
import LoginForm from '../src/components/LoginForm';

const App: React.FC = () => {

  const handleLogin = (username: string, password: string) => {

    console.log("Login attempt with:", username, password);
  };

  const handleLoginWithGoogle = () => {

    console.log("Login with Google requested");
  };

  const handleLoginWithFacebook = () => {

    console.log("Login with Facebook requested");
  };

  return (
    <ChakraProvider>
      {}
      <LoginForm
        onLogin={handleLogin}
        onLoginWithGoogle={handleLoginWithGoogle}
        onLoginWithFacebook={handleLoginWithFacebook}
      />
    </ChakraProvider>
  );
}

export default App;
