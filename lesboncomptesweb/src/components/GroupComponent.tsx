import React, { useState } from 'react';
import {
  Box,
  Tabs,
  TabList,
  TabPanels,
  Tab,
  TabPanel
} from '@chakra-ui/react';

interface GroupData {
  id: string;
  name: string;

}

interface GroupComponentProps {
  groupData: GroupData;
}

const GroupComponent: React.FC<GroupComponentProps> = ({ groupData }) => {
  const [selectedTab, setSelectedTab] = useState(0);

  return (
    <Box p={5} shadow="md" borderWidth="1px">
      <Tabs index={selectedTab} onChange={(index) => setSelectedTab(index)}>
        <TabList>
          <Tab>Dépenses</Tab>
          <Tab>Soldes</Tab>
          <Tab>Remboursements</Tab>
          <Tab>Messages</Tab>
        </TabList>

        <TabPanels>
          <TabPanel>
            <p>Contenu des dépenses...</p>
          </TabPanel>
          <TabPanel>
            <p>Contenu des soldes...</p>
          </TabPanel>
          <TabPanel>
            <p>Contenu des remboursements...</p>
          </TabPanel>
          <TabPanel>
            <p>Contenu des messages...</p>
          </TabPanel>
        </TabPanels>
      </Tabs>
    </Box>
  );
};

export default GroupComponent;
