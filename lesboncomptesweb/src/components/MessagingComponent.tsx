import React, { useState, useEffect } from 'react';
import {
  Box,
  Button,
  FormControl,
  FormLabel,
  Textarea,
  VStack,
  Tabs,
  TabList,
  TabPanels,
  Tab,
  TabPanel,
  Select,
  useBreakpointValue,
  Text,
  useToast,
} from '@chakra-ui/react';
import axios from 'axios';

interface User {
  id: string;
  username: string;
}

interface MessagingProps {
  groupId: string;
  userId: string;
  users: User[];
}

interface Message {
  id: string;
  content: string;
  sender: { id: string; username: string };
  recipient?: { id: string; username: string };
  timestamp: string;
}

const MessagingComponent: React.FC<MessagingProps> = ({ groupId, userId, users }) => {
  const [message, setMessage] = useState('');
  const [recipient, setRecipient] = useState<string | undefined>(undefined);
  const [messages, setMessages] = useState<Message[]>([]);
  const toast = useToast();
  const formWidth = useBreakpointValue({ base: '100%', md: '100%' });

  useEffect(() => {
    fetchMessages();
  }, [groupId]);

  const fetchMessages = async () => {
    try {
      const token = localStorage.getItem('jwt');
      const response = await axios.get(`http://localhost:5000/messaging/group_messages/${groupId}`, {
        headers: { Authorization: `Bearer ${token}` },
      });
      setMessages(response.data);
    } catch (error) {
      toast({
        title: 'Failed to fetch messages',
        description: error.response?.data?.message || 'Could not fetch messages',
        status: 'error',
        duration: 5000,
        isClosable: true,
      });
    }
  };

  const handleSendMessage = async () => {
    if (!message.trim()) return;

    const token = localStorage.getItem('jwt');
    const config = { headers: { Authorization: `Bearer ${token}` } };

    const url = recipient
      ? `http://localhost:5000/messaging/send_private_message`
      : `http://localhost:5000/messaging/send_group_message`;

    const payload = recipient
      ? {
          content: message,
          recipient_username: recipient,
        }
      : {
          content: message,
          group_id: groupId,
        };

    try {
      await axios.post(url, payload, config);
      setMessage('');
      setRecipient(undefined);
      fetchMessages();
    } catch (error) {
      toast({
        title: 'Failed to send message',
        description: error.response?.data?.message || 'Could not send message',
        status: 'error',
        duration: 5000,
        isClosable: true,
      });
    }
  };

  return (
    <Box p={5} shadow="md" borderWidth="1px" width={formWidth}>
      <Tabs>
        <TabList>
          <Tab>Group Chat</Tab>
          <Tab>Private Messages</Tab>
        </TabList>
        <TabPanels>
          <TabPanel>
            <VStack spacing={4} align="stretch">
              <FormControl>
                <FormLabel>Message</FormLabel>
                <Textarea
                  placeholder="Write a message..."
                  value={message}
                  onChange={(e) => setMessage(e.target.value)}
                />
              </FormControl>
              <Button colorScheme="blue" onClick={handleSendMessage}>Send</Button>
              {messages.filter(msg => !msg.recipient).map((msg) => (
                <Box key={msg.id} p={3} shadow="md" borderWidth="1px">
                  <Text><strong>{msg.sender.username}</strong> ({new Date(msg.timestamp).toLocaleString()}):</Text>
                  <Text>{msg.content}</Text>
                </Box>
              ))}
            </VStack>
          </TabPanel>
          <TabPanel>
            <VStack spacing={4} align="stretch">
              <FormControl>
                <FormLabel>Recipient</FormLabel>
                <Select placeholder="Select recipient" value={recipient} onChange={(e) => setRecipient(e.target.value)}>
                  {users.map((user) => (
                    <option key={user.id} value={user.username}>{user.username}</option>
                  ))}
                </Select>
              </FormControl>
              <FormControl>
                <FormLabel>Message</FormLabel>
                <Textarea
                  placeholder="Write a private message..."
                  value={message}
                  onChange={(e) => setMessage(e.target.value)}
                />
              </FormControl>
              <Button colorScheme="blue" onClick={handleSendMessage}>Send</Button>
              {messages.filter(msg => msg.recipient).map((msg) => (
                <Box key={msg.id} p={3} shadow="md" borderWidth="1px">
                  <Text><strong>{msg.sender.username}</strong> to <strong>{msg.recipient?.username}</strong> ({new Date(msg.timestamp).toLocaleString()}):</Text>
                  <Text>{msg.content}</Text>
                </Box>
              ))}
            </VStack>
          </TabPanel>
        </TabPanels>
      </Tabs>
    </Box>
  );
};

export default MessagingComponent;
