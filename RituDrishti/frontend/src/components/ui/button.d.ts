import * as React from 'react';
export const Button: React.ForwardRefExoticComponent<React.ButtonHTMLAttributes<HTMLButtonElement> & {variant?:string;size?:string;asChild?:boolean} & React.RefAttributes<HTMLButtonElement>>;
export const buttonVariants: (props?:Record<string,unknown>)=>string;