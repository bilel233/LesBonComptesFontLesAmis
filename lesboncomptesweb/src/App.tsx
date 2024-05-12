import React, { useState, useEffect } from 'react';
import { ChakraProvider, Box, Text, VStack } from '@chakra-ui/react';
import LoginForm from './components/LoginForm';
import GroupComponent from './components/GroupComponent';
import CreateGroupForm from './components/CreateGroupForm';

interface User {
  username: string;
  id: string;
}

interface GroupData {
  id: string;
  name: string;
}

const App: React.FC = () => {
  const [user, setUser] = useState<User | null>(null);
  const [groups, setGroups] = useState<GroupData[]>([]);

  const handleLogin = (username: string, userId: string) => {
    setUser({ username, id: userId });
  };

  const handleLoginWithGoogle = () => {

  };

  const handleLoginWithFacebook = () => {

  };

  const handleCreateGroup = (group: GroupData) => {
    setGroups([...groups, group]);
  };

  return (
    <ChakraProvider>
      {!user ? (
        <LoginForm
          onLogin={(username) => handleLogin(username, 'some-user-id')}
          onLoginWithGoogle={handleLoginWithGoogle}
          onLoginWithFacebook={handleLoginWithFacebook}
        />
      ) : (
        <VStack spacing={4}>
          <Text>Welcome, {user.username}</Text>
          <CreateGroupForm onCreate={handleCreateGroup} />
          {groups.map(group => (
            <GroupComponent key={group.id} groupData={group} userId={user.id} />
          ))}
        </VStack>
      )}
    </ChakraProvider>
  );
};

export default App;
