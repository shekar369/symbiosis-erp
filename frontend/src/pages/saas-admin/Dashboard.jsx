import { useEffect, useState } from 'react'
import { StatsGrid } from '@/components/StatsGrid'
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"
import { SubscriptionList, InvoiceList } from '@/components/billing/BillingComponents'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { RecentRegistrations } from '@/components/registrations/RecentRegistrations'
import { Button } from '@/components/ui/button'
import api from '../../api/axios'

export default function SaasAdminDashboard() {
  const [dashboardData, setDashboardData] = useState(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)

  useEffect(() => {
    const fetchDashboardData = async () => {
      try {
        const response = await api.get('/admin/saas-admin/dashboard')
        setDashboardData(response.data)
        setLoading(false)
      } catch (err) {
        setError(err.message)
        setLoading(false)
      }
    }

    fetchDashboardData()
  }, [])

  if (loading) return <div>Loading...</div>
  if (error) return <div>Error: {error}</div>

  return (
    <div className="flex-1 space-y-4 p-4 md:p-8 pt-6">
      <div className="flex items-center justify-between space-y-2">
        <h2 className="text-3xl font-bold tracking-tight">Dashboard</h2>
        <div className="flex items-center space-x-2">
          <Button>Download Report</Button>
        </div>
      </div>

      <StatsGrid stats={dashboardData.dashboard_data} />

      <Tabs defaultValue="overview" className="space-y-4">
        <TabsList>
          <TabsTrigger value="overview">Overview</TabsTrigger>
          <TabsTrigger value="subscriptions">Subscriptions</TabsTrigger>
          <TabsTrigger value="billing">Billing</TabsTrigger>
          <TabsTrigger value="registrations">Registrations</TabsTrigger>
        </TabsList>

        <TabsContent value="overview" className="space-y-4">
          <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
            <Card>
              <CardHeader>
                <CardTitle>Recent Activity</CardTitle>
              </CardHeader>
              <CardContent>
                {/* Add activity feed component */}
              </CardContent>
            </Card>

            <Card className="col-span-2">
              <CardHeader>
                <CardTitle>Revenue Overview</CardTitle>
              </CardHeader>
              <CardContent>
                {/* Add revenue chart component */}
              </CardContent>
            </Card>

            <Card>
              <CardHeader>
                <CardTitle>Quick Actions</CardTitle>
              </CardHeader>
              <CardContent className="space-y-2">
                <Button className="w-full" variant="outline">
                  New Tenant
                </Button>
                <Button className="w-full" variant="outline">
                  Create Invoice
                </Button>
                <Button className="w-full" variant="outline">
                  View Reports
                </Button>
              </CardContent>
            </Card>
          </div>
        </TabsContent>

        <TabsContent value="subscriptions">
          <Card>
            <CardHeader>
              <CardTitle>Active Subscriptions</CardTitle>
              <CardDescription>Manage tenant subscriptions and plans</CardDescription>
            </CardHeader>
            <CardContent>
              <SubscriptionList subscriptions={dashboardData.subscriptions} />
            </CardContent>
          </Card>
        </TabsContent>

        <TabsContent value="billing">
          <Card>
            <CardHeader>
              <CardTitle>Billing & Invoices</CardTitle>
              <CardDescription>Track payments and manage invoices</CardDescription>
            </CardHeader>
            <CardContent>
              <InvoiceList invoices={dashboardData.recent_invoices} />
            </CardContent>
          </Card>
        </TabsContent>

        <TabsContent value="registrations">
          <Card>
            <CardHeader>
              <CardTitle>Recent Registrations</CardTitle>
              <CardDescription>Review and approve organization registrations</CardDescription>
            </CardHeader>
            <CardContent>
              <RecentRegistrations registrations={dashboardData.recent_registrations} />
            </CardContent>
          </Card>
        </TabsContent>
      </Tabs>
    </div>
  )
}
