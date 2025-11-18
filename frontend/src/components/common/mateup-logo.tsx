export const MateUpLogo = (props: React.ComponentProps<"svg">) => (
  <svg
    viewBox="0 0 420 160"
    fill="currentColor"
    xmlns="http://www.w3.org/2000/svg"
    {...props}
  >
    <g
      textAnchor="middle"
      fontFamily="Inter, sans-serif"
      dominantBaseline="middle"
    >
      {/* MATE */}
      <text
        x="30%"
        y="45%"
        fontWeight="900"
        fontSize="72"
        opacity="0.8"
        letterSpacing="6px"
      >
        mate
      </text>

      {/* UP */}
      <text
        x="75%"
        y="45%"
        className="text-[#0ACACA] animate-pulse duration-1000 ease-in-out"
        fontWeight="900"
        fontSize="100"
        letterSpacing="6px"
      >
        Up
      </text>
    </g>
    {/* LEAGUE */}{" "}
    <text
      x="60%"
      y="90%"
      textAnchor="middle"
      fontFamily="Inter, sans-serif"
      fontWeight="800"
      fontSize="50"
      opacity="0.8"
      letterSpacing="8px"
      dominantBaseline="middle"
      fill="#ae0538"
    >
      LEAGUE
    </text>
  </svg>
);
