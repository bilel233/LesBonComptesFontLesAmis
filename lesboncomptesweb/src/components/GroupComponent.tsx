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
}

interface GroupComponentProps {
  groupData: GroupData;
  userId: string;
}

const GroupComponent: React.FC<GroupComponentProps> = ({ groupData, userId }) => {
  const [selectedTab, setSelectedTab] = useState<number>(0);
  const [users, setUsers] = useState<User[]>([]);

  useEffect(() => {
    fetchGroupUsers();
  }, [groupData.id]);

  const fetchGroupUsers = async () => {
    try {
      const token = localStorage.getItem('jwt');
      const response = await axios.get(`http://localhost:5000/group/${groupData.id}`, {
        headers: { Authorization: `Bearer ${token}` }
      });
      setUsers(response.data.members);
    } catch (error) {
      console.error("Error fetching group users:", error);
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
          <TabPanel>
            <GroupExpenses groupId={groupData.id} />
          </TabPanel>
          <TabPanel>
            <CreateExpenseForm groupId={groupData.id} users={users} onCreate={fetchGroupUsers} />
          </TabPanel>
          <TabPanel>
            <GroupBalances groupId={groupData.id} />
          </TabPanel>
          <TabPanel><p>Contenu des remboursements...</p></TabPanel>
          <TabPanel>
            <MessagingComponent groupId={groupData.id} userId={userId} />
          </TabPanel>
          <TabPanel>
            <InviteMembersForm groupId={groupData.id} />
          </TabPanel>
        </TabPanels>
      </Tabs>
    </Box>
  );
};

export default GroupComponent;
