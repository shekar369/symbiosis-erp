import React, { useState, useEffect } from 'react';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import api from '../../api/axios';
import { toast } from 'react-hot-toast';
import {
  Card,
  Heading,
  Text,
  Button,
  Select,
  Input,
  Switch,
  Table,
  Tbody,
  Tr,
  Td,
  Badge,
  HStack,
  VStack,
  useDisclosure,
  Modal,
  ModalOverlay,
  ModalContent,
  ModalHeader,
  ModalBody,
  ModalFooter,
  ModalCloseButton,
  FormControl,
  FormLabel,
  Textarea,
} from '@chakra-ui/react';

const ConfigurationList = () => {
  const queryClient = useQueryClient();
  const { isOpen, onOpen, onClose } = useDisclosure();
  const [selectedConfig, setSelectedConfig] = useState(null);
  const [editMode, setEditMode] = useState(false);
  const [filter, setFilter] = useState('ALL');

  const { data: configs, isLoading, isError, error } = useQuery({
    queryKey: ['configurations'],
    queryFn: () => api.get('/config').then(r => r.data),
    enabled: Boolean(localStorage.getItem('accessToken')), // Only fetch if authenticated
  });

  const updateMutation = useMutation({
    mutationFn: (data) =>
      api.patch(`/config/${data.id}`, data.update).then(r => r.data),
    onSuccess: () => {
      queryClient.invalidateQueries(['configurations']);
      toast.success('Configuration updated successfully');
      onClose();
    },
    onError: (error) => {
      toast.error(error.message || 'Failed to update configuration');
    },
  });

  const handleEdit = (config) => {
    setSelectedConfig(config);
    setEditMode(true);
    onOpen();
  };

  const handleView = (config) => {
    setSelectedConfig(config);
    setEditMode(false);
    onOpen();
  };

  const handleUpdate = async (formData) => {
    updateMutation.mutate({
      id: selectedConfig.id,
      update: formData,
    });
  };

  const filteredConfigs = configs?.filter(
    (config) => filter === 'ALL' || config.category === filter
  ) || [];

  if (isLoading) {
    return <Text>Loading configurations...</Text>;
  }

  if (isError) {
    if (error?.response?.status === 401) {
      return <Text>Please log in to view configurations.</Text>;
    }
    return <Text>Error loading configurations: {error.message}</Text>;
  }

  if (!configs) {
    return <Text>No configurations found.</Text>;
  }

  return (
    <VStack spacing={6} align="stretch" w="full">
      <Card p={6}>
        <VStack spacing={4} align="stretch">
          <HStack justify="space-between">
            <Heading size="md">System Configurations</Heading>
            <Select
              w="200px"
              value={filter}
              onChange={(e) => setFilter(e.target.value)}
            >
              <option value="ALL">All Categories</option>
              <option value="EMAIL">Email</option>
              <option value="SECURITY">Security</option>
              <option value="BILLING">Billing</option>
              <option value="NOTIFICATION">Notification</option>
              <option value="SYSTEM">System</option>
            </Select>
          </HStack>

          <Table variant="simple">
            <Tbody>
              {filteredConfigs.map((config) => (
                <Tr key={config.id}>
                  <Td>
                    <VStack align="start" spacing={1}>
                      <Text fontWeight="medium">{config.key}</Text>
                      <Text fontSize="sm" color="gray.600">
                        {config.description}
                      </Text>
                    </VStack>
                  </Td>
                  <Td>
                    <Badge colorScheme={getBadgeColor(config.category)}>
                      {config.category}
                    </Badge>
                  </Td>
                  <Td textAlign="right">
                    <HStack spacing={2} justify="flex-end">
                      <Button
                        size="sm"
                        variant="ghost"
                        onClick={() => handleView(config)}
                      >
                        View
                      </Button>
                      <Button
                        size="sm"
                        colorScheme="blue"
                        onClick={() => handleEdit(config)}
                      >
                        Edit
                      </Button>
                    </HStack>
                  </Td>
                </Tr>
              ))}
            </Tbody>
          </Table>
        </VStack>
      </Card>

      <ConfigurationModal
        isOpen={isOpen}
        onClose={() => {
          onClose();
          setSelectedConfig(null);
          setEditMode(false);
        }}
        config={selectedConfig}
        isEditing={editMode}
        onUpdate={handleUpdate}
      />
    </VStack>
  );
};

const ConfigurationModal = ({ isOpen, onClose, config, isEditing, onUpdate }) => {
  const [formData, setFormData] = useState({
    value: '',
    description: '',
    is_active: true,
  });

  useEffect(() => {
    if (config) {
      setFormData({
        value: config.value || '',
        description: config.description || '',
        is_active: config.is_active,
      });
    }
  }, [config]);

  const handleSubmit = (e) => {
    e.preventDefault();
    onUpdate(formData);
  };

  return (
    <Modal isOpen={isOpen} onClose={onClose} size="xl">
      <ModalOverlay />
      <ModalContent>
        <ModalHeader>
          {isEditing ? 'Edit Configuration' : 'View Configuration'}
        </ModalHeader>
        <ModalCloseButton />
        <form onSubmit={handleSubmit}>
          <ModalBody>
            <VStack spacing={4} align="stretch">
              {config && (
                <>
                  <FormControl>
                    <FormLabel>Key</FormLabel>
                    <Input value={config.key} isReadOnly />
                  </FormControl>

                  <FormControl>
                    <FormLabel>Category</FormLabel>
                    <Input value={config.category} isReadOnly />
                  </FormControl>

                  <FormControl>
                    <FormLabel>Value</FormLabel>
                    {config.is_encrypted ? (
                      <Input
                        type="password"
                        value={formData.value}
                        onChange={(e) =>
                          setFormData({ ...formData, value: e.target.value })
                        }
                        isReadOnly={!isEditing}
                      />
                    ) : (
                      <Textarea
                        value={formData.value}
                        onChange={(e) =>
                          setFormData({ ...formData, value: e.target.value })
                        }
                        isReadOnly={!isEditing}
                      />
                    )}
                  </FormControl>

                  <FormControl>
                    <FormLabel>Description</FormLabel>
                    <Textarea
                      value={formData.description}
                      onChange={(e) =>
                        setFormData({ ...formData, description: e.target.value })
                      }
                      isReadOnly={!isEditing}
                    />
                  </FormControl>

                  <FormControl>
                    <FormLabel>Status</FormLabel>
                    <Switch
                      isChecked={formData.is_active}
                      onChange={(e) =>
                        setFormData({
                          ...formData,
                          is_active: e.target.checked,
                        })
                      }
                      isDisabled={!isEditing}
                    />
                  </FormControl>
                </>
              )}
            </VStack>
          </ModalBody>
          <ModalFooter>
            <Button variant="ghost" mr={3} onClick={onClose}>
              Cancel
            </Button>
            {isEditing && (
              <Button type="submit" colorScheme="blue">
                Save Changes
              </Button>
            )}
          </ModalFooter>
        </form>
      </ModalContent>
    </Modal>
  );
};

const getBadgeColor = (category) => {
  const colors = {
    EMAIL: 'blue',
    SECURITY: 'red',
    BILLING: 'green',
    NOTIFICATION: 'purple',
    SYSTEM: 'orange',
  };
  return colors[category] || 'gray';
};

export default ConfigurationList;
