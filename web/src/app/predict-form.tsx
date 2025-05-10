"use client";

import { zodResolver } from "@hookform/resolvers/zod";
import { useForm } from "react-hook-form";
import { z } from "zod";

import { Button } from "~/components/ui/button";
import {
  Form,
  FormControl,
  FormDescription,
  FormField,
  FormItem,
  FormLabel,
  FormMessage,
} from "~/components/ui/form";
import { Input } from "~/components/ui/input";
import { ScrollArea } from "~/components/ui/scroll-area";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "~/components/ui/select";
import type { Prediction } from "./page";
import { useCallback } from "react";

const formSchema = z.object({
  kills: z.coerce
    .number()
    .min(0, { message: "Kills must be greater than 0" })
    .max(100, { message: "Kills must be less than 100" }),
  total_minion_kills: z.coerce
    .number()
    .min(0, { message: "Total minion kills must be greater than 0" })
    .max(1500, { message: "Total minion kills must be less than 1500" }),
  assist: z.coerce
    .number()
    .min(0, { message: "Assists must be greater than 0" })
    .max(300, { message: "Assists must be less than 300" }),
  baron_kills: z.coerce
    .number()
    .min(0, { message: "Baron kills must be greater than 0" })
    .max(6, { message: "Baron kills must be less than 6" }),
  tower_kills: z.coerce
    .number()
    .min(0, { message: "Tower kills must be greater than 0" })
    .max(14, { message: "Tower kills must be less than 14" }),
  dragon_kills: z.coerce
    .number()
    .min(0, { message: "Dragon kills must be greater than 0" })
    .max(10, { message: "Dragon kills must be less than 10" }),
  game_duration: z.coerce
    .number()
    .min(0, { message: "Game duration must be greater than 0" })
    .max(3600, { message: "Game duration must be less than 3600 seconds" }),
  death: z.coerce
    .number()
    .min(0, { message: "Deaths must be greater than 0" })
    .max(110, { message: "Deaths must be less than 110" }),
});

const featureNames = [
  "kills",
  "total_minion_kills",
  "assist",
  "baron_kills",
  "tower_kills",
  "dragon_kills",
  "game_duration",
  "death",
] as const;

export function PredictForm({
  setPrediction,
}: {
  setPrediction: React.Dispatch<React.SetStateAction<Prediction | null>>;
}) {
  const form = useForm<z.infer<typeof formSchema>>({
    resolver: zodResolver(formSchema),
    defaultValues: {
      kills: 0,
      total_minion_kills: 0,
      assist: 0,
      baron_kills: 0,
      tower_kills: 0,
      dragon_kills: 0,
      game_duration: 0,
      death: 0,
    },
  });

  const getFeildLabel = useCallback((feature: string) => {
    switch (feature) {
      case "kills":
        return "Kills";
      case "total_minion_kills":
        return "Total Minion Kills";
      case "assist":
        return "Assists";
      case "baron_kills":
        return "Baron Kills";
      case "tower_kills":
        return "Tower Kills";
      case "dragon_kills":
        return "Dragon Kills";
      case "game_duration":
        return "Game Duration (seconds)";
      case "death":
        return "Deaths";
      default:
        return feature;
    }
  }, []);

  async function onSubmit(values: z.infer<typeof formSchema>) {
    console.log(values);
    const response = await fetch("http://localhost:8000/api/predict", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(values),
    });

    const data = (await response.json()) as Prediction;
    setPrediction(data);
  }

  return (
    <Form {...form}>
      <form onSubmit={form.handleSubmit(onSubmit)} className="space-y-8">
        <ScrollArea className="h-[350px]">
          <div className="space-y-4 p-4">
            {featureNames.map((feature) => (
              <FormField
                control={form.control}
                key={feature}
                name={feature}
                render={({ field }) => (
                  <FormItem>
                    <FormLabel>{getFeildLabel(feature)}</FormLabel>
                    <Input type="number" {...field} />
                    <FormMessage />
                  </FormItem>
                )}
              />
            ))}
          </div>
        </ScrollArea>
        <Button
          type="submit"
          className="w-full"
          disabled={form.formState.isSubmitting}
        >
          {form.formState.isSubmitting ? "Predicting..." : "Predict"}
        </Button>
      </form>
    </Form>
  );
}
