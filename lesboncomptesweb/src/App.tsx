
// src/App.tsx
import React, { useState, useEffect } from 'react';
import { ChakraProvider, VStack, Text, useToast, theme } from '@chakra-ui/react';
import axios from 'axios';
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
  const toast = useToast();

  const handleLogin = async (username: string, userId: string) => {
    setUser({ username, id: userId });
    await fetchGroups(username);
  };

  const fetchGroups = async (username: string) => {
    const token = localStorage.getItem('jwt');
    if (!token) {
      toast({
        title: 'Erreur d\'authentification',
        description: 'Veuillez vous reconnecter.',
        status: 'error',
        duration: 5000,
        isClosable: true,
      });
      return;
    }

    try {
      const response = await axios.get(`http://localhost:5000/group/user/${username}`, {
        headers: { Authorization: `Bearer ${token}` }
      });
      setGroups(response.data);
    } catch (error) {
      toast({
        title: 'Échec de la récupération des groupes',
        description: error.response?.data?.message || 'Une erreur inattendue est survenue',
        status: 'error',
        duration: 5000,
        isClosable: true,
      });
    }
  };

  const handleCreateGroup = (group: GroupData) => {
    setGroups([...groups, group]);
  };

  const handleLoginWithFacebook = () => {
    // La logique de connexion Facebook est gérée directement dans le composant LoginForm.
  };

  return (
  <ChakraProvider theme={theme}>
    {!user ? (
      <LoginForm
        onLogin={handleLogin}
        onLoginWithGoogle={() => {}}
        onLoginWithFacebook={handleLoginWithFacebook}
      />
    ) : (
      <VStack spacing={4}>
        <Text>Bienvenue, {user.username}</Text>
        <CreateGroupForm onCreate={handleCreateGroup} />
        {groups.map(group => (
          <GroupComponent key={group.id} userId={user.id} /> // Removed groupData
        ))}
      </VStack>
    )}
  </ChakraProvider>
);
};

export default App;
