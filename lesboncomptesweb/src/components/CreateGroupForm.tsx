import React, { useState } from 'react';
import {
  Box,
  Button,
  FormControl,
  FormLabel,
  Input,
  useToast
} from '@chakra-ui/react';
import axios from 'axios';

interface GroupData {
  id: string;
  name: string;
}

interface CreateGroupFormProps {
  onCreate: (group: GroupData) => void;
}

const CreateGroupForm: React.FC<CreateGroupFormProps> = ({ onCreate }) => {
  const [groupName, setGroupName] = useState<string>('');
  const toast = useToast();

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

  try {
    const response = await axios.post('http://localhost:5000/group/create', { name: groupName }, {
      headers: {
        Authorization: `Bearer ${token}`
      }
    });

    console.log("Response data:", response.data);

    if (response.data && response.data.name && response.data.group_id) {
      toast({
        title: 'Group Created',
        description: `You have created "${response.data.name}".`,
        status: 'success',
        duration: 5000,
        isClosable: true,
      });
      onCreate({ id: response.data.group_id, name: response.data.name });
    } else {
      throw new Error('Invalid response data');
    }
  } catch (error) {
    console.error("Error details:", error.response || error);
    toast({
      title: 'Failed to create group',
      description: error.response?.data?.message || "Unexpected error occurred",
      status: 'error',
      duration: 5000,
      isClosable: true,
    });
  }
};


  return (
    <Box p={5} shadow="md" borderWidth="1px">
      <FormControl isRequired>
        <FormLabel>Name of the Group</FormLabel>
        <Input
          placeholder="Enter group name"
          value={groupName}
          onChange={(e) => setGroupName(e.target.value)}
        />
      </FormControl>
      <Button mt={4} colorScheme="blue" onClick={handleSubmit}>
        Create Group
      </Button>
    </Box>
  );
};

export default CreateGroupForm;
