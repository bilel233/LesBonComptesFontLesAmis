import React, { useState } from 'react';
import {
  Box,
  Button,
  FormControl,
  FormLabel,
  Input,
  useToast,
  VStack,
  useBreakpointValue,
  Textarea
} from '@chakra-ui/react';
import axios from 'axios';

interface InviteMembersProps {
  groupId: string;
}

const InviteMembersForm: React.FC<InviteMembersProps> = ({ groupId }) => {
  const [usernames, setUsernames] = useState<string>('');
  const toast = useToast();
  const apiUrl = 'http://localhost:5000';

  const handleInviteMembers = async () => {
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
      const response = await axios.post(`${apiUrl}/group/${groupId}/invite`, { usernames: usernames.split(',') }, {
        headers: { Authorization: `Bearer ${token}` }
      });

      if (response.data) {
        toast({
          title: 'Invitation Sent',
          description: 'Members have been invited successfully.',
          status: 'success',
          duration: 5000,
          isClosable: true,
        });
      }
    } catch (error) {
      toast({
        title: 'Failed to Invite Members',
        description: error.response?.data?.message || "Unexpected error occurred",
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
          <Textarea
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
