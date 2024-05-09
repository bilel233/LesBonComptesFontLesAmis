import * as React from 'react';
import { ChakraProvider } from '@chakra-ui/react';

const App: React.FC = () => {
  return (
    <ChakraProvider>
      <div>Hello World</div>
    </ChakraProvider>
  );
}

export default App;
