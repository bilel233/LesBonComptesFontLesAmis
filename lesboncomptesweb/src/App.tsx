// App.tsx
import React, { useState, useEffect } from 'react';
import { ChakraProvider, Box, Text, VStack } from '@chakra-ui/react';
import LoginForm from './components/LoginForm';
import GroupComponent from './components/GroupComponent';
import CreateGroupForm from './components/CreateGroupForm';

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
    // Implémentez la logique pour récupérer les groupes ici
  };

  const handleLogin = (username: string) => {
    setUser({ username });
  };

  const handleCreateGroup = (group: GroupData) => {
    setGroups([...groups, group]); // Ajouter le nouveau groupe à la liste
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
        <VStack spacing={4}>
          <Box>
            <Text>Welcome, {user.username}</Text>
            <CreateGroupForm onCreate={handleCreateGroup} />
          </Box>
          {groups.map(group => (
            <GroupComponent key={group.id} groupData={group} />
          ))}
        </VStack>
      )}
    </ChakraProvider>
  );
};

export default App;
