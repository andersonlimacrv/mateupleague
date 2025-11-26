
import React from 'react';
import { createPortal } from "react-dom";
import { Button } from '@/components/ui/button';
import { cn } from '@/lib/utils';
import { MenuToggleIcon } from '@/components/ui/menu-toggle-icon';
import { useScroll } from '@/hooks/useScroll';
import type { LinkItem } from "@/types/components/link-item-navbar-header";
import { MateUpLogo } from "@/components/common/mateup-logo";
import {
  productLinks,
  companyLinks,
  companyLinks2,
} from "@/lib/constants/navbar-header";
import {
  NavigationMenu,
  NavigationMenuContent,
  NavigationMenuItem,
  NavigationMenuLink,
  NavigationMenuList,
  NavigationMenuTrigger,
} from "@/components/ui/navigation-menu";

export function Header() {
	const [open, setOpen] = React.useState(false);
	const scrolled = useScroll(10);

	React.useEffect(() => {
    if (open) {
      document.body.style.overflow = "hidden";
    } else {
      document.body.style.overflow = "";
    }
    return () => {
      document.body.style.overflow = "";
    };
  }, [open]);

	return (
    <header
      className={cn(
        "sticky top-0 z-50 mx-auto w-full max-w-5xl border-b border-transparent md:rounded-md md:border md:transition-all md:ease-out",
        {
          "bg-background/95 supports-backdrop-filter:bg-background/50 border-border backdrop-blur-lg md:top-4 md:max-w-4xl md:shadow":
            scrolled && !open,
          "bg-background/90": open,
        }
      )}
    >
      <nav
        className={cn(
          "flex h-14 w-full items-center justify-between px-4 md:h-12 md:transition-all md:ease-out",
          {
            "md:px-2 py-7": scrolled,
          }
        )}
      >
        <div className="flex items-center">
          <MateUpLogo className="h-8" />
          <p className="-rotate-45">🚀</p>
        </div>
        <NavigationMenu className="hidden md:flex">
          <NavigationMenuList>
            <NavigationMenuItem>
              <NavigationMenuTrigger className="bg-transparent">
                Product
              </NavigationMenuTrigger>
              <NavigationMenuContent className="bg-background p-1 pr-1.5">
                <ul className="bg-popover grid w-lg grid-cols-2 gap-2 rounded-md border p-2 shadow">
                  {productLinks.map((item, i) => (
                    <li key={i}>
                      <ListItem {...item} />
                    </li>
                  ))}
                </ul>
                <div className="p-2">
                  <p className="text-muted-foreground text-sm">
                    Interested?{" "}
                    <a
                      href="#"
                      className="text-foreground font-medium hover:underline"
                    >
                      Schedule a demo
                    </a>
                  </p>
                </div>
              </NavigationMenuContent>
            </NavigationMenuItem>
            <NavigationMenuItem>
              <NavigationMenuTrigger className="bg-transparent">
                Company
              </NavigationMenuTrigger>
              <NavigationMenuContent className="bg-background p-1 pr-1.5 pb-1.5">
                <div className="grid w-lg grid-cols-2 gap-2">
                  <ul className="bg-popover space-y-2 rounded-md border p-2 shadow">
                    {companyLinks.map((item, i) => (
                      <li key={i}>
                        <ListItem {...item} />
                      </li>
                    ))}
                  </ul>
                  <ul className="space-y-2 p-3">
                    {companyLinks2.map((item, i) => (
                      <li key={i}>
                        <NavigationMenuLink
                          href={item.href}
                          className="flex p-2 hover:bg-accent flex-row rounded-md items-center gap-x-2"
                        >
                          <item.icon className="text-foreground size-4 drop-shadow-black/80 drop-shadow" />
                          <span className="font-medium drop-shadow-black/80 drop-shadow">
                            {item.title}
                          </span>
                        </NavigationMenuLink>
                      </li>
                    ))}
                  </ul>
                </div>
              </NavigationMenuContent>
            </NavigationMenuItem>
            <NavigationMenuLink className="px-4" asChild>
              <a href="#" className="hover:bg-accent rounded-md py-1.5">
                <p className="drop-shadow-black/80 drop-shadow">Pricing</p>
              </a>
            </NavigationMenuLink>
          </NavigationMenuList>
        </NavigationMenu>
        <div className="hidden items-center gap-2 md:flex">
          <Button variant="outline">Sign In</Button>
          <Button>Get Started</Button>
        </div>
        <Button
          size="icon"
          variant="outline"
          onClick={() => setOpen(!open)}
          className="md:hidden"
          aria-expanded={open}
          aria-controls="mobile-menu"
          aria-label="Toggle menu"
        >
          <MenuToggleIcon open={open} className="size-5" duration={300} />
        </Button>
      </nav>

      <MobileMenu
        open={open}
        className="flex flex-col justify-between gap-2 overflow-y-auto"
      >
        <NavigationMenu className="max-w-full">
          <div className="flex w-full flex-col gap-y-2">
            <span className="text-sm">Product</span>
            {productLinks.map((link) => (
              <ListItem key={link.title} {...link} />
            ))}
            <span className="text-sm">Company</span>
            {companyLinks.map((link) => (
              <ListItem key={link.title} {...link} />
            ))}
            {companyLinks2.map((link) => (
              <ListItem key={link.title} {...link} />
            ))}
          </div>
        </NavigationMenu>
        <div className="flex flex-col gap-2">
          <Button variant="outline" className="w-full bg-transparent">
            Sign In
          </Button>
          <Button className="w-full">Get Started</Button>
        </div>
      </MobileMenu>
    </header>
  );
}

type MobileMenuProps = React.ComponentProps<'div'> & {
  open: boolean;
};

function MobileMenu({ open, children, className, ...props }: MobileMenuProps) {
  if (!open || typeof window === 'undefined') return null;

  return createPortal(
    <div
      id="mobile-menu"
      className={cn(
        "bg-background/90 supports-backdrop-filter:bg-background/50 backdrop-blur-md",
        "fixed top-14 right-0 bottom-0 left-0 z-40 flex flex-col overflow-hidden border-y md:hidden"
      )}
    >
      <div
        data-slot={open ? "open" : "closed"}
        className={cn(
          "data-[slot=open]:animate-in data-[slot=open]:zoom-in-97 ease-out",
          "size-full p-4",
          className
        )}
        {...props}
      >
        {children}
      </div>
    </div>,
    document.body
  );
}

function ListItem({
  title,
  description,
  icon: Icon,
  className,
  href,
  ...props
}: React.ComponentProps<typeof NavigationMenuLink> & LinkItem) {
  return (
    <NavigationMenuLink
      className={cn(
        "w-full flex flex-row gap-x-2 data-[active=true]:focus:bg-accent data-[active=true]:hover:bg-accent data-[active=true]:bg-accent/50 data-[active=true]:text-accent-foreground hover:bg-accent hover:text-accent-foreground focus:bg-accent focus:text-accent-foreground rounded-sm p-2",
        className
      )}
      {...props}
      asChild
    >
      <a href={href} className="group">
        <div className="bg-background/40 flex aspect-square size-12 items-center justify-center rounded-md border shadow-sm">
          <Icon className="text-foreground size-5" />
        </div>
        <div className="flex flex-col items-start justify-center">
          <span className="font-medium">{title}</span>
          <span className="text-foreground text-sm drop-shadow-black/90 drop-shadow">{description}</span>
        </div>
      </a>
    </NavigationMenuLink>
  );
}