
import React, { useState, useEffect } from 'react';
import { ChakraProvider, Box, Text } from '@chakra-ui/react';
import LoginForm from './components/LoginForm';
import GroupComponent from './components/GroupComponent';

interface User {
  username: string;
}

interface GroupData {
  id: string;
  name: string;
}

const App: React.FC = () => {
  const [user, setUser] = useState<User | null>(null);
  const [groups, setGroups] = useState<GroupData[]>([]);

  useEffect(() => {
    if (user) {
      fetchGroups();
    }
  }, [user]);

  const fetchGroups = async () => {
    // ...
  };

  const handleLogin = (username: string) => {
    setUser({ username });
  };

  return (
    <ChakraProvider>
      {!user ? (
        <LoginForm
          onLogin={handleLogin}
          onLoginWithGoogle={() => {}}
          onLoginWithFacebook={() => {}}
        />
      ) : (
        <Box>
          <Text>Welcome, {user.username}</Text>
          {groups.map(group => (
            <GroupComponent key={group.id} groupData={group} />
          ))}
        </Box>
      )}
    </ChakraProvider>
  );
};

export default App;
