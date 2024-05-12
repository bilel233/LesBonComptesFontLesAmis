import React, { useState, useEffect } from 'react';
import { Box, Text, VStack, useToast } from '@chakra-ui/react';
import axios from 'axios';

interface BalanceProps {
  groupId: string;
}

interface Balances {
  [username: string]: number;
}

const GroupBalances: React.FC<BalanceProps> = ({ groupId }) => {
  const [balances, setBalances] = useState<Balances>({});
  const toast = useToast();

  useEffect(() => {
    const fetchBalances = async () => {
      try {
        const token = localStorage.getItem('jwt');
        const response = await axios.get<{balances: Balances}>(`http://localhost:5000/group/${groupId}/balances`, {
          headers: { Authorization: `Bearer ${token}` }
        });
        setBalances(response.data.balances);
      } catch (error) {
        toast({
          title: 'Failed to fetch balances',
          description: error.response?.data?.message || "Could not fetch balances",
          status: 'error',
          duration: 5000,
          isClosable: true,
        });
      }
    };

    fetchBalances();
  }, [groupId, toast]);

  return (
    <VStack spacing={4} align="stretch">
      {Object.entries(balances).map(([username, balance]) => (
        <Box key={username} p={4} shadow="md" borderWidth="1px">
          <Text>{username}: {balance.toFixed(2)} €</Text>
        </Box>
      ))}
    </VStack>
  );
};

export default GroupBalances;
