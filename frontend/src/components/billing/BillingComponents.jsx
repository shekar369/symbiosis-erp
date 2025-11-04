import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from "./ui/card"
import { Button } from "./ui/button"
import { Badge } from "./ui/badge"

export function PricingCard({ plan }) {
  return (
    <Card className="flex flex-col">
      <CardHeader>
        <CardTitle>{plan.name}</CardTitle>
        <CardDescription>{plan.description}</CardDescription>
      </CardHeader>
      <CardContent className="flex-grow">
        <div className="mt-4 flex flex-col gap-4">
          <div className="flex items-baseline">
            <span className="text-3xl font-bold">${plan.price_monthly}</span>
            <span className="ml-1 text-gray-500">/month</span>
          </div>
          <div className="space-y-2">
            {plan.features.map((feature) => (
              <div key={feature.name} className="flex items-center">
                <CheckIcon className="mr-2 h-4 w-4 text-green-500" />
                <span>{feature.value}</span>
              </div>
            ))}
          </div>
        </div>
      </CardContent>
      <CardFooter>
        <Button className="w-full">Select Plan</Button>
      </CardFooter>
    </Card>
  )
}

export function SubscriptionList({ subscriptions }) {
  return (
    <div className="space-y-4">
      {subscriptions.map((subscription) => (
        <Card key={subscription.id}>
          <CardHeader className="pb-2">
            <div className="flex items-center justify-between">
              <CardTitle className="text-lg">
                {subscription.tenant.name}
              </CardTitle>
              <Badge variant={getStatusVariant(subscription.status)}>
                {subscription.status}
              </Badge>
            </div>
          </CardHeader>
          <CardContent>
            <div className="grid gap-2">
              <div className="flex justify-between text-sm">
                <span className="text-muted-foreground">Plan:</span>
                <span className="font-medium">{subscription.plan.name}</span>
              </div>
              <div className="flex justify-between text-sm">
                <span className="text-muted-foreground">Billing:</span>
                <span className="font-medium">{subscription.billing_interval}</span>
              </div>
              <div className="flex justify-between text-sm">
                <span className="text-muted-foreground">Next Payment:</span>
                <span className="font-medium">
                  {new Date(subscription.current_period_end).toLocaleDateString()}
                </span>
              </div>
            </div>
          </CardContent>
          <CardFooter className="flex justify-end space-x-2">
            <Button variant="outline" size="sm">View Details</Button>
            <Button variant="default" size="sm">Manage</Button>
          </CardFooter>
        </Card>
      ))}
    </div>
  )
}

export function InvoiceList({ invoices }) {
  return (
    <div className="space-y-4">
      {invoices.map((invoice) => (
        <Card key={invoice.id}>
          <CardHeader className="pb-2">
            <div className="flex items-center justify-between">
              <CardTitle className="text-lg">Invoice #{invoice.id}</CardTitle>
              <Badge variant={getInvoiceStatusVariant(invoice.status)}>
                {invoice.status}
              </Badge>
            </div>
          </CardHeader>
          <CardContent>
            <div className="grid gap-2">
              <div className="flex justify-between text-sm">
                <span className="text-muted-foreground">Amount:</span>
                <span className="font-medium">${invoice.amount}</span>
              </div>
              <div className="flex justify-between text-sm">
                <span className="text-muted-foreground">Due Date:</span>
                <span className="font-medium">
                  {new Date(invoice.due_date).toLocaleDateString()}
                </span>
              </div>
              <div className="flex justify-between text-sm">
                <span className="text-muted-foreground">Organization:</span>
                <span className="font-medium">{invoice.tenant.name}</span>
              </div>
            </div>
          </CardContent>
          <CardFooter className="flex justify-end space-x-2">
            <Button variant="outline" size="sm">Download</Button>
            {invoice.status === 'unpaid' && (
              <Button variant="default" size="sm">Mark as Paid</Button>
            )}
          </CardFooter>
        </Card>
      ))}
    </div>
  )
}

function getStatusVariant(status) {
  switch (status) {
    case 'active':
      return 'success'
    case 'trial':
      return 'warning'
    case 'past_due':
      return 'destructive'
    case 'canceled':
      return 'secondary'
    default:
      return 'default'
  }
}

function getInvoiceStatusVariant(status) {
  switch (status) {
    case 'paid':
      return 'success'
    case 'unpaid':
      return 'warning'
    case 'overdue':
      return 'destructive'
    default:
      return 'default'
  }
}

function CheckIcon(props) {
  return (
    <svg
      {...props}
      xmlns="http://www.w3.org/2000/svg"
      width="24"
      height="24"
      viewBox="0 0 24 24"
      fill="none"
      stroke="currentColor"
      strokeWidth="2"
      strokeLinecap="round"
      strokeLinejoin="round"
    >
      <polyline points="20 6 9 17 4 12" />
    </svg>
  )
}