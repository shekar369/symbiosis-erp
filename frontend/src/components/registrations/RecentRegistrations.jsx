import { Card, CardContent, CardFooter, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Badge } from "@/components/ui/badge"
import api from "../../api/axios"
import { toast } from "@/components/ui/use-toast"

export function RecentRegistrations({ registrations }) {
  const handleApprove = async (registrationId) => {
    try {
      await api.put(`/registrations/${registrationId}/review`, {
        status: 'approved',
        review_notes: 'Approved by admin'
      })
      toast({
        title: "Registration Approved",
        description: "The organization registration has been approved."
      })
    } catch (error) {
      toast({
        title: "Error",
        description: "Failed to approve registration.",
        variant: "destructive"
      })
    }
  }

  const handleReject = async (registrationId) => {
    try {
      await api.put(`/registrations/${registrationId}/review`, {
        status: 'rejected',
        review_notes: 'Rejected by admin'
      })
      toast({
        title: "Registration Rejected",
        description: "The organization registration has been rejected."
      })
    } catch (error) {
      toast({
        title: "Error",
        description: "Failed to reject registration.",
        variant: "destructive"
      })
    }
  }

  return (
    <div className="space-y-4">
      {registrations.map((registration) => (
        <Card key={registration.id}>
          <CardHeader>
            <div className="flex items-center justify-between">
              <CardTitle className="text-lg">{registration.name}</CardTitle>
              <Badge variant={getStatusVariant(registration.status)}>
                {registration.status}
              </Badge>
            </div>
          </CardHeader>
          <CardContent>
            <div className="grid gap-2">
              <div className="grid grid-cols-2 gap-4">
                <div>
                  <p className="text-sm font-medium text-muted-foreground">Contact Person</p>
                  <p className="text-sm">{registration.contact_person}</p>
                </div>
                <div>
                  <p className="text-sm font-medium text-muted-foreground">Email</p>
                  <p className="text-sm">{registration.email}</p>
                </div>
                <div>
                  <p className="text-sm font-medium text-muted-foreground">Business Type</p>
                  <p className="text-sm">{registration.business_type}</p>
                </div>
                <div>
                  <p className="text-sm font-medium text-muted-foreground">Employee Count</p>
                  <p className="text-sm">{registration.employee_count}</p>
                </div>
              </div>
              {registration.notes && (
                <div className="mt-2">
                  <p className="text-sm font-medium text-muted-foreground">Notes</p>
                  <p className="text-sm">{registration.notes}</p>
                </div>
              )}
            </div>
          </CardContent>
          {registration.status === 'pending' && (
            <CardFooter className="flex justify-end space-x-2">
              <Button
                variant="outline"
                onClick={() => handleReject(registration.id)}
              >
                Reject
              </Button>
              <Button
                variant="default"
                onClick={() => handleApprove(registration.id)}
              >
                Approve
              </Button>
            </CardFooter>
          )}
        </Card>
      ))}
    </div>
  )
}

function getStatusVariant(status) {
  switch (status) {
    case 'approved':
      return 'success'
    case 'pending':
      return 'warning'
    case 'rejected':
      return 'destructive'
    default:
      return 'default'
  }
}
