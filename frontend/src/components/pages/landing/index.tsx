import { motion } from "framer-motion";
import type {FormEvent } from "react";
import {
  bannerVariants,
  headlineVariants,
  subHeadlineVariants,
  formVariants,
  trialTextVariants,
  worksWithVariants,
  imageVariants,
} from "@/components/common/animations/variants";
import { ShinyText } from "@/components/ui/shiny-text";
import { RotatingText } from "@/components/ui/rotating-text";
import { Button } from "@/components/ui/button";


export default function LandingPage() {
  return (
    <main className="flex- flex flex-col items-center justify-center text-center px-4 pt-8 pb-16 relative z-10">
      <motion.div
        variants={bannerVariants}
        initial="hidden"
        animate="visible"
        className="mb-6"
      >
        <ShinyText
          text="Announcing our $15M Series A"
          className="bg-[#1a1a1a] border border-gray-700 text-accent px-4 py-1 rounded-full text-xs sm:text-sm font-medium cursor-pointer hover:border-accent/50 transition-colors"
        />
      </motion.div>

      <motion.h1
        variants={headlineVariants}
        initial="hidden"
        animate="visible"
        className="text-4xl sm:text-5xl lg:text-[64px] font-semibold text-foreground leading-tight max-w-4xl mb-4"
      >
        Deliver collaborative
        <br />{" "}
        <span className="inline-block h-[1.2em] sm:h-[1.2em] lg:h-[1.2em] overflow-hidden align-bottom">
          <RotatingText
            texts={[
              "Support",
              "Experiences",
              "Relationships",
              "Help",
              "Service",
            ]}
            mainClassName="text-accent mx-1"
            staggerFrom={"last"}
            initial={{ y: "-100%", opacity: 0 }}
            animate={{ y: 0, opacity: 1 }}
            exit={{ y: "110%", opacity: 0 }}
            staggerDuration={0.01}
            transition={{ type: "spring", damping: 18, stiffness: 250 }}
            rotationInterval={2200}
            splitBy="characters"
            auto={true}
            loop={true}
          />
        </span>
      </motion.h1>

      <motion.p
        variants={subHeadlineVariants}
        initial="hidden"
        animate="visible"
        className="text-base sm:text-lg lg:text-xl text-gray-400 max-w-2xl mx-auto mb-8"
      >
        Support your customers on Slack, Microsoft Teams, Discord and many more
        – and move from answering tickets to building genuine relationships.
      </motion.p>

      <motion.form
        variants={formVariants}
        initial="hidden"
        animate="visible"
        className="flex flex-col sm:flex-row items-center justify-center gap-2 w-full max-w-md mx-auto mb-3"
        onSubmit={(e: FormEvent<HTMLFormElement>) => e.preventDefault()}
      >
        <input
          type="email"
          placeholder="Your work email"
          required
          aria-label="Work Email"
          className="grow w-full sm:w-auto px-4 py-2 rounded-md bg-[#2a2a2a] border border-gray-700 text-white placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-accent focus:border-transparent transition-all"
        />
        <Button variant="default">colocar algum botão bonito</Button>
      </motion.form>

      <motion.p
        variants={trialTextVariants}
        initial="hidden"
        animate="visible"
        className="text-xs text-muted-foreground mb-10"
      >
        Free 14 day trial
      </motion.p>

      <motion.div
        variants={worksWithVariants}
        initial="hidden"
        animate="visible"
        className="flex flex-col items-center justify-center space-y-2 mb-10"
      >
        <>colocar alguma coisa</>
      </motion.div>

      <motion.div
        variants={imageVariants}
        initial="hidden"
        animate="visible"
        className="w-full max-w-4xl mx-auto px-4 sm:px-0"
      >
        <img
          src="https://help.apple.com/assets/679AD2D1E874AD22770DE1E0/679AD2D56EA7B10C9E01288F/en_US/3d2b57c8027ae355aa44421899389008.png"
          alt="Product screen preview showing collaborative features"
          width={1024}
          height={640}
          className="w-full h-auto object-contain rounded-lg shadow-xl border border-border"
          loading="lazy"
        />
      </motion.div>
    </main>
  );
}

