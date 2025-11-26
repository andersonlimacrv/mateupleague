import type { Variants } from "framer-motion";
const contentDelay = 0.3;
const itemDelayIncrement = 0.1;

const bannerVariants: Variants = {
  hidden: { opacity: 0, y: -10 },
  visible: {
    opacity: 1,
    y: 0,
    transition: { duration: 0.4, delay: contentDelay },
  },
};
const headlineVariants: Variants = {
  hidden: { opacity: 0 },
  visible: {
    opacity: 1,
    transition: { duration: 0.5, delay: contentDelay + itemDelayIncrement },
  },
};
const subHeadlineVariants: Variants = {
  hidden: { opacity: 0, y: 10 },
  visible: {
    opacity: 1,
    y: 0,
    transition: { duration: 0.5, delay: contentDelay + itemDelayIncrement * 2 },
  },
};
const formVariants: Variants = {
  hidden: { opacity: 0, y: 10 },
  visible: {
    opacity: 1,
    y: 0,
    transition: { duration: 0.5, delay: contentDelay + itemDelayIncrement * 3 },
  },
};
const trialTextVariants: Variants = {
  hidden: { opacity: 0 },
  visible: {
    opacity: 1,
    transition: { duration: 0.5, delay: contentDelay + itemDelayIncrement * 4 },
  },
};
const worksWithVariants: Variants = {
  hidden: { opacity: 0 },
  visible: {
    opacity: 1,
    transition: { duration: 0.5, delay: contentDelay + itemDelayIncrement * 5 },
  },
};
const imageVariants: Variants = {
  hidden: { opacity: 0, scale: 0.95, y: 20 },
  visible: {
    opacity: 1,
    scale: 1,
    y: 0,
    transition: {
      duration: 0.6,
      delay: contentDelay + itemDelayIncrement * 6,
      ease: [0.16, 1, 0.3, 1],
    },
  },
};

export {
  bannerVariants,
  headlineVariants,
  subHeadlineVariants,
  formVariants,
  trialTextVariants,
  worksWithVariants,
  imageVariants,
};