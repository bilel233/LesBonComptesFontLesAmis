import React, { useState, useEffect } from 'react';
import {
  Box,
  Button,
  Flex,
  Select,
  VStack,
  useToast,
  Text
} from '@chakra-ui/react';
import axios from 'axios';

interface Expense {
  id: string;
  title: string;
  amount: number;
  date: string;
  payer: string;
  category: string;
  involved_members: string[];
  weights: number[];
  group: string;
}

interface ExpenseProps {
  groupId: string;
}

const GroupExpenses: React.FC<ExpenseProps> = ({ groupId }) => {
  const [expenses, setExpenses] = useState<Expense[]>([]);
  const [sortBy, setSortBy] = useState<string>('date');
  const toast = useToast();

  useEffect(() => {
    fetchExpenses();
  }, [groupId, sortBy]);

  const fetchExpenses = async () => {
    try {
      const token = localStorage.getItem('jwt');
      const response = await axios.get(`http://localhost:5000/expenses/get_all_expenses`, {
        headers: { Authorization: `Bearer ${token}` }
      });
      let expenses = response.data.filter((expense: Expense) => expense.group === groupId);

      switch (sortBy) {
        case 'amount':
          expenses.sort((a: Expense, b: Expense) => b.amount - a.amount);
          break;
        case 'payer':
          expenses.sort((a: Expense, b: Expense) => a.payer.localeCompare(b.payer));
          break;
        default:
          expenses.sort((a: Expense, b: Expense) => new Date(b.date).getTime() - new Date(a.date).getTime());
      }

      setExpenses(expenses);
    } catch (error) {
      toast({
        title: 'Failed to fetch expenses',
        description: error.response?.data?.message || "Could not fetch expenses",
        status: 'error',
        duration: 5000,
        isClosable: true,
      });
    }
  };

  return (
    <VStack spacing={4} align="stretch">
      <Flex justify="space-between" width="100%">
        <Text fontSize="xl">Dépenses</Text>
        <Select width="200px" value={sortBy} onChange={(e) => setSortBy(e.target.value)}>
          <option value="date">Date</option>
          <option value="amount">Montant</option>
          <option value="payer">Membre</option>
        </Select>
      </Flex>
      {expenses.map((expense) => (
        <Box key={expense.id} p={4} shadow="md" borderWidth="1px">
          <Text>Intitulé: {expense.title}</Text>
          <Text>Montant: {expense.amount} €</Text>
          <Text>Date: {expense.date}</Text>
          <Text>Payeur: {expense.payer}</Text>
          <Text>Catégorie: {expense.category}</Text>
          <Text>Membres impliqués: {expense.involved_members.join(', ')}</Text>
        </Box>
      ))}
    </VStack>
  );
};

export default GroupExpenses;
