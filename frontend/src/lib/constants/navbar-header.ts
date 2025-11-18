import {
  CodeIcon,
  GlobeIcon,
  LayersIcon,
  UserPlusIcon,
  Users,
  Star,
  FileText,
  Shield,
  RotateCcw,
  Handshake,
  Leaf,
  HelpCircle,
  BarChart,
  PlugIcon,
} from "lucide-react";
import type { LinkItem } from "@/types/components/link-item-navbar-header";

export const productLinks: LinkItem[] = [
  {
    title: "Website Builder",
    href: "#",
    description: "Create responsive websites with ease",
    icon: GlobeIcon,
  },
  {
    title: "Cloud Platform",
    href: "#",
    description: "Deploy and scale apps in the cloud",
    icon: LayersIcon,
  },
  {
    title: "Team Collaboration",
    href: "#",
    description: "Tools to help your teams work better together",
    icon: UserPlusIcon,
  },
  {
    title: "Analytics",
    href: "#",
    description: "Track and analyze your website traffic",
    icon: BarChart,
  },
  {
    title: "Integrations",
    href: "#",
    description: "Connect your apps and services",
    icon: PlugIcon,
  },
  {
    title: "API",
    href: "#",
    description: "Build custom integrations with our API",
    icon: CodeIcon,
  },
];

export const companyLinks: LinkItem[] = [
  {
    title: "About Us",
    href: "#",
    description: "Learn more about our story and team",
    icon: Users,
  },
  {
    title: "Customer Stories",
    href: "#",
    description: "See how we’ve helped our clients succeed",
    icon: Star,
  },
  {
    title: "Partnerships",
    href: "#",
    icon: Handshake,
    description: "Collaborate with us for mutual growth",
  },
];

export const companyLinks2: LinkItem[] = [
  {
    title: "Terms of Service",
    href: "#",
    icon: FileText,
  },
  {
    title: "Privacy Policy",
    href: "#",
    icon: Shield,
  },
  {
    title: "Refund Policy",
    href: "#",
    icon: RotateCcw,
  },
  {
    title: "Blog",
    href: "#",
    icon: Leaf,
  },
  {
    title: "Help Center",
    href: "#",
    icon: HelpCircle,
  },
];
