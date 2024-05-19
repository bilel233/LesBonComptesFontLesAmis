import React, { useState, useEffect, ChangeEvent } from 'react';
import {
  Box,
  Button,
  FormControl,
  FormLabel,
  Input,
  Select,
  Textarea,
  VStack,
  useToast,
  CheckboxGroup,
  Checkbox,
  NumberInput,
  NumberInputField,
  Stack,
  useBreakpointValue
} from '@chakra-ui/react';
import axios from 'axios';

const categories = ['Alimentation', 'Frais de déplacement', 'Activité', 'Autre'];

interface User {
  username: string;
  id: string;
}

interface CreateExpenseFormProps {
  groupId: string;
  users: User[];
  onCreate: () => void;
}

const CreateExpenseForm: React.FC<CreateExpenseFormProps> = ({ groupId, users, onCreate }) => {
  const [title, setTitle] = useState<string>('');
  const [amount, setAmount] = useState<number>(0);
  const [date, setDate] = useState<string>('');
  const [category, setCategory] = useState<string>(categories[0]);
  const [selectedUsers, setSelectedUsers] = useState<string[]>([]);
  const [weights, setWeights] = useState<number[]>([]);
  const [file, setFile] = useState<File | null>(null);
  const toast = useToast();
  const formWidth = useBreakpointValue({ base: "100%", md: "100%" });

  useEffect(() => {
    setWeights(new Array(selectedUsers.length).fill(1));
  }, [selectedUsers]);

  const handleFileChange = (event: ChangeEvent<HTMLInputElement>) => {
    if (event.target.files) {
      setFile(event.target.files[0]);
    }
  };

  const handleSubmit = async () => {
  const token = localStorage.getItem('jwt');
  if (!token) {
    toast({
      title: 'Authentication Error',
      description: 'No token found, please login again.',
      status: 'error',
      duration: 5000,
      isClosable: true,
    });
    return;
  }

  const formData = new FormData();
  formData.append('title', title);
  formData.append('amount', amount.toString());
  formData.append('date', date);
  formData.append('category', category);
  formData.append('group_id', groupId);
  formData.append('involved_members', JSON.stringify(selectedUsers)); // Convert to JSON
  formData.append('weights', JSON.stringify(weights)); // Convert to JSON
  if (file) {
    formData.append('receipt', file);
  }

  try {
    const response = await axios.post('http://localhost:5000/expenses/create_expense', formData, {
      headers: {
        Authorization: `Bearer ${token}`,
        'Content-Type': 'multipart/form-data'
      }
    });

    toast({
      title: 'Expense Created',
      description: 'Your expense has been created successfully.',
      status: 'success',
      duration: 5000,
      isClosable: true,
    });
    onCreate();
  } catch (error) {
    toast({
      title: 'Failed to create expense',
      description: error.response?.data?.message || "Unexpected error occurred",
      status: 'error',
      duration: 5000,
      isClosable: true,
    });
  }
};

  return (
    <Box p={5} shadow="md" borderWidth="1px" width={formWidth}>
      <VStack spacing={4}>
        <FormControl isRequired>
          <FormLabel>Intitulé</FormLabel>
          <Input
            placeholder="Enter expense title"
            value={title}
            onChange={(e) => setTitle(e.target.value)}
          />
        </FormControl>
        <FormControl isRequired>
          <FormLabel>Montant</FormLabel>
          <NumberInput value={amount} onChange={(valueString) => setAmount(parseFloat(valueString))}>
            <NumberInputField />
          </NumberInput>
        </FormControl>
        <FormControl isRequired>
          <FormLabel>Date</FormLabel>
          <Input
            type="date"
            value={date}
            onChange={(e) => setDate(e.target.value)}
          />
        </FormControl>
        <FormControl isRequired>
          <FormLabel>Catégorie</FormLabel>
          <Select value={category} onChange={(e) => setCategory(e.target.value)}>
            {categories.map((cat) => (
              <option key={cat} value={cat}>{cat}</option>
            ))}
          </Select>
        </FormControl>
        <FormControl isRequired>
          <FormLabel>Membres impliqués</FormLabel>
          <CheckboxGroup value={selectedUsers} onChange={(values) => setSelectedUsers(values as string[])}>
            <Stack spacing={5} direction="column">
              {users.map((user) => (
                <Checkbox key={user.id} value={user.id}>
                  {user.username}
                </Checkbox>
              ))}
            </Stack>
          </CheckboxGroup>
        </FormControl>
        <FormControl>
          <FormLabel>Justificatif</FormLabel>
          <Input type="file" accept="application/pdf, image/*" onChange={handleFileChange} />
        </FormControl>
        <Button colorScheme="blue" onClick={handleSubmit}>
          Déclarer la dépense
        </Button>
      </VStack>
    </Box>
  );
};

export default CreateExpenseForm;
