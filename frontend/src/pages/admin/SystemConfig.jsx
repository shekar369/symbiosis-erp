import React from 'react';
import {
  Container,
  Heading,
  Text,
  VStack,
  HStack,
  Card,
  CardBody,
  Icon,
  Button,
} from '@chakra-ui/react';
import { MdSettings, MdRefresh } from 'react-icons/md';
import { useMutation, useQueryClient } from '@tanstack/react-query';
import { fetchApi } from '../../utils/api';
import { toast } from 'react-hot-toast';
import ConfigurationList from '../../components/admin/ConfigurationList';

const SystemConfigPage = () => {
  const queryClient = useQueryClient();

  const initializeMutation = useMutation({
    mutationFn: () => fetchApi('/config/initialize', { method: 'POST' }),
    onSuccess: () => {
      queryClient.invalidateQueries(['configurations']);
      toast.success('Default configurations initialized successfully');
    },
    onError: (error) => {
      toast.error(error.message || 'Failed to initialize configurations');
    },
  });

  return (
    <Container maxW="container.xl" py={8}>
      <VStack spacing={6} align="stretch">
        <HStack justify="space-between">
          <HStack>
            <Icon as={MdSettings} boxSize={6} color="blue.500" />
            <Heading size="lg">System Configuration</Heading>
          </HStack>
          <Button
            leftIcon={<MdRefresh />}
            colorScheme="blue"
            variant="outline"
            onClick={() => initializeMutation.mutate()}
            isLoading={initializeMutation.isLoading}
          >
            Initialize Defaults
          </Button>
        </HStack>

        <Card>
          <CardBody>
            <Text color="gray.600" mb={6}>
              Manage system-wide configuration settings. Changes made here will
              affect the entire application. Please be careful when modifying these
              settings.
            </Text>
            <ConfigurationList />
          </CardBody>
        </Card>
      </VStack>
    </Container>
  );
};

export default SystemConfigPage;