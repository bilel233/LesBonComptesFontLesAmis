import React, { useState } from 'react';
import {
  Box,
  Tabs,
  TabList,
  TabPanels,
  Tab,
  TabPanel
} from '@chakra-ui/react';
import MessagingComponent from '../components/MessagingComponent';
import InviteMembersForm from './InviteMembersForm';
import GroupBalances from './GroupBalances';

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

  return (
    <Box p={5} shadow="md" borderWidth="1px">
      <Tabs index={selectedTab} onChange={(index) => setSelectedTab(index)}>
        <TabList>
          <Tab>Dépenses</Tab>
          <Tab>Soldes</Tab>
          <Tab>Remboursements</Tab>
          <Tab>Messages</Tab>
          <Tab>Inviter</Tab>
        </TabList>

        <TabPanels>
          <TabPanel><p>Contenu des dépenses...</p></TabPanel>
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
