import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "./ui/card"
import { BarChart, Users, Building2, CreditCard } from "../../utils/icons"

const statCards = [
  {
    title: "Total Revenue",
    value: "$45,231.89",
    description: "Monthly revenue",
    icon: BarChart,
    change: "+20.1%",
    changeType: "positive"
  },
  {
    title: "Active Tenants",
    value: "245",
    description: "Total organizations",
    icon: Building2,
    change: "+18.5%",
    changeType: "positive"
  },
  {
    title: "Total Users",
    value: "2,350",
    description: "Across all tenants",
    icon: Users,
    change: "+7.2%",
    changeType: "positive"
  },
  {
    title: "Pending Invoices",
    value: "12",
    description: "Worth $15,234.00",
    icon: CreditCard,
    change: "-4.5%",
    changeType: "negative"
  }
]

export function StatsGrid() {
  return (
    <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
      {statCards.map((stat) => (
        <Card key={stat.title}>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">
              {stat.title}
            </CardTitle>
            <stat.icon className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{stat.value}</div>
            <p className="text-xs text-muted-foreground">
              {stat.description}
            </p>
            <div className={`mt-2 text-xs ${
              stat.changeType === 'positive' ? 'text-green-600' : 'text-red-600'
            }`}>
              {stat.change}
            </div>
          </CardContent>
        </Card>
      ))}
    </div>
  )
}