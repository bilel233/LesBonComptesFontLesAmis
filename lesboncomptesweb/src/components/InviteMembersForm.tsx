import React, { useState } from 'react';
import {
  Box,
  Button,
  FormControl,
  FormLabel,
  Input,
  VStack,
  useToast
} from '@chakra-ui/react';
import axios from 'axios';

interface InviteMembersFormProps {
  groupName: string;
}

const InviteMembersForm: React.FC<InviteMembersFormProps> = ({ groupName }) => {
  const [usernames, setUsernames] = useState('');
  const toast = useToast();
  const token = localStorage.getItem('jwt');

  const handleInviteMembers = async () => {
    if (!token) {
      toast({
        title: 'Authentication Error',
        description: 'Please log in to invite members.',
        status: 'error',
        duration: 5000,
        isClosable: true,
      });
      return;
    }

    const payload = {
      group_name: groupName,
      usernames: usernames.split(',').map(username => username.trim())
    };

    try {
      await axios.post('http://localhost:5000/group/invite', payload, {
        headers: { Authorization: `Bearer ${token}` }
      });

      toast({
        title: 'Invitation Sent',
        description: 'Members have been invited successfully.',
        status: 'success',
        duration: 5000,
        isClosable: true,
      });
      setUsernames('');
    } catch (error) {
      toast({
        title: 'Failed to Invite Members',
        description: error.response?.data?.message || 'Unexpected error occurred',
        status: 'error',
        duration: 5000,
        isClosable: true,
      });
    }
  };

  return (
    <Box p={5} shadow="md" borderWidth="1px">
      <VStack spacing={4}>
        <FormControl isRequired>
          <FormLabel>Invite Members</FormLabel>
          <Input
            placeholder="Enter usernames separated by commas"
            value={usernames}
            onChange={(e) => setUsernames(e.target.value)}
          />
        </FormControl>
        <Button colorScheme="blue" onClick={handleInviteMembers}>
          Send Invites
        </Button>
      </VStack>
    </Box>
  );
};

export default InviteMembersForm;
