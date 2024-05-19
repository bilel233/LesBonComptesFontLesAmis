import React, { useState, useEffect } from 'react';
import { Box, Tabs, TabList, TabPanels, Tab, TabPanel } from '@chakra-ui/react';
import MessagingComponent from '../components/MessagingComponent';
import InviteMembersForm from './InviteMembersForm';
import GroupBalances from './GroupBalances';
import GroupExpenses from './GroupExpenses';
import CreateExpenseForm from './CreateExpenseForm';
import axios from 'axios';

interface User {
  username: string;
  id: string;
}

interface GroupData {
  id: string;
  name: string;
  creator: string;
  members: User[];
}

interface GroupComponentProps {
  userId: string; // Only userId is needed now since we are fetching all groups for the user
}

const GroupComponent: React.FC<GroupComponentProps> = ({ userId }) => {
  const [selectedTab, setSelectedTab] = useState<number>(0);
  const [groups, setGroups] = useState<GroupData[]>([]);

  useEffect(() => {
    fetchUserGroups();
  }, [userId]);

  const fetchUserGroups = async () => {
    const token = localStorage.getItem('jwt');
    try {
      const response = await axios.get<GroupData[]>(`http://localhost:5000/group/user/${userId}`, {
        headers: { Authorization: `Bearer ${token}` }
      });
      setGroups(response.data);
    } catch (error) {
      console.error("Error fetching user groups:", error);
    }
  };

  return (
    <Box p={5} shadow="md" borderWidth="1px">
      <Tabs index={selectedTab} onChange={(index) => setSelectedTab(index)}>
        <TabList>
          <Tab>Dépenses</Tab>
          <Tab>Déclarer une Dépense</Tab>
          <Tab>Soldes</Tab>
          <Tab>Remboursements</Tab>
          <Tab>Messages</Tab>
          <Tab>Inviter</Tab>
        </TabList>

        <TabPanels>
          {groups.map(group => (
            <TabPanel key={group.id}>
              <GroupExpenses groupId={group.id} />
              <CreateExpenseForm groupId={group.id} users={group.members} onCreate={() => fetchUserGroups()} />
              <GroupBalances groupId={group.id} />
              <MessagingComponent groupId={group.id} userId={userId} users={group.members} />
              <InviteMembersForm groupId={group.id} />
            </TabPanel>
          ))}
        </TabPanels>
      </Tabs>
    </Box>
  );
};

export default GroupComponent;
