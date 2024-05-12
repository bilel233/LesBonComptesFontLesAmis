import React, { useState, useEffect } from 'react';
import {
  Box,
  Button,
  FormControl,
  FormLabel,
  Input,
  VStack,
  Textarea,
  useToast
} from '@chakra-ui/react';
import axios from 'axios';

interface MessagingProps {
  groupId: string;
  userId: string;
}

interface Message {
  id: string;
  content: string;
  senderId: string;
  timestamp?: Date;
}

const MessagingComponent: React.FC<MessagingProps> = ({ groupId, userId }) => {
  const [message, setMessage] = useState('');
  const [recipient, setRecipient] = useState(''); // For private messages
  const [messages, setMessages] = useState<Message[]>([]);
  const toast = useToast();

  useEffect(() => {
    fetchMessages();
  }, [groupId]);

  const fetchMessages = async () => {
    const url = `http://localhost:5000/messaging/${groupId}/group_messages`;
    try {
      const response = await axios.get(url);
      setMessages(response.data);
    } catch (error) {
      toast({
        title: 'Error Fetching Messages',
        description: error.response?.data?.message || "Could not fetch messages",
        status: 'error',
        duration: 5000,
        isClosable: true,
      });
    }
  };

  const handleSendMessage = async () => {
    if (!message.trim()) return;

    const token = localStorage.getItem('jwt'); // Assuming token is stored in localStorage
    const config = {
        headers: {
            Authorization: `Bearer ${token}`
        }
    };

    const url = recipient
        ? `http://localhost:5000/messaging/send_private_message`
        : `http://localhost:5000/messaging/send_group_message`;

    const payload = {
        content: message,
        senderId: userId,
        groupId: recipient ? undefined : groupId,
        recipientUsername: recipient || undefined
    };

    try {
        const response = await axios.post(url, payload, config);
        if (response.status === 201) {
            setMessage('');
            setRecipient('');
            fetchMessages();  // Refresh the messages
        }
    } catch (error) {
        toast({
            title: 'Error Sending Message',
            description: error.response?.data?.message || "Could not send message",
            status: 'error',
            duration: 5000,
            isClosable: true,
        });
    }
};

  return (
    <Box p={5}>
      <VStack spacing={4}>
        <FormControl>
          <FormLabel htmlFor='message'>Message</FormLabel>
          <Textarea
            id='message'
            placeholder="Write a message..."
            value={message}
            onChange={(e) => setMessage(e.target.value)}
          />
        </FormControl>
        <FormControl>
          <FormLabel htmlFor='recipient'>Recipient (for private messages)</FormLabel>
          <Input
            id='recipient'
            placeholder="Recipient username"
            value={recipient}
            onChange={(e) => setRecipient(e.target.value)}
          />
        </FormControl>
        <Button colorScheme="blue" onClick={handleSendMessage}>
          Send Message
        </Button>
        {messages.map((msg, index) => (
          <Box key={index} p={3} shadow="md" borderWidth="1px">
            {msg.content}
          </Box>
        ))}
      </VStack>
    </Box>
  );
};

export default MessagingComponent;
