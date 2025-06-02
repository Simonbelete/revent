"use client";
import React, { useEffect, useState } from "react";
import {
  Modal,
  Form,
  Input,
  DatePicker,
  Layout,
  Menu,
  MenuProps,
  Checkbox,
  Select,
  Button,
} from "antd";
import dayjs from "dayjs";
import { PrimaryHeader } from "@/components/common/headers";
import { CalendarOutlined } from "@ant-design/icons";

import { Calendar, momentLocalizer } from "react-big-calendar";
import moment from "moment";
import Sider from "antd/es/layout/Sider";
import useSWR from "swr";
import { apiGET, apiPOST } from "@/lib/api_call";
import { CalendarModel, ExpandEvent } from "@/models";
import { useWatch } from "antd/es/form/Form";
import useSWRMutation from "swr/mutation";
import { useRouter } from "next/navigation";

const localizer = momentLocalizer(moment);

const { Content } = Layout;
const { RangePicker } = DatePicker;

interface Event {
  title: string;
  date: string;
  description?: string;
}

export default function HomePage() {
  const router = useRouter();

  const [currentDate, setCurrentDate] = useState(moment()); // Use moment object
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [activeCalendar, setActiveCalendar] = useState<string>("");

  const [form] = Form.useForm();
  const watch_relative_weekday =
    useWatch("relative_weekday", form)?.label ?? "";
  const watch_recurrence: boolean = useWatch("recurrence", form) ?? false;

  useEffect(() => {
    console.log(watch_recurrence);
  }, [watch_recurrence]);

  const years = Array.from({ length: 20 }, (_, i) => moment().year() - 10 + i);
  const months = moment.months(); // ['January', 'February', ..., 'December']

  const { trigger } = useSWRMutation("/events/", apiPOST);

  const handleYearChange = (e: React.ChangeEvent<HTMLSelectElement>) => {
    const newYear = parseInt(e.target.value);
    const updated = currentDate.clone().year(newYear);
    setCurrentDate(updated);
  };

  const handleMonthChange = (e: React.ChangeEvent<HTMLSelectElement>) => {
    const newMonth = parseInt(e.target.value); // 0-indexed
    const updated = currentDate.clone().month(newMonth);
    setCurrentDate(updated);
  };

  const handleOk = () => {
    form
      .validateFields()
      .then((values) => {
        const newEvent: Event = {
          ...values,
          // date: values.date.format("YYYY-MM-DD"),
          start_datetime: values?.date[0],
          end_datetime: values?.date[1],
          relative_weekday: values?.relative_weekday?.value,
          calendar: Number(activeCalendar),
        };

        trigger(newEvent);
        setIsModalOpen(false);
        form.resetFields();
      })
      .catch((err) => console.log(err));
  };

  const { data: calendarsData } = useSWR<CalendarModel[], Error>(
    "calendars/",
    apiGET
  );
  const { data: eventsData } = useSWR<ExpandEvent[], Error>(
    `calendars/${activeCalendar}/expand`,
    apiGET
  );
  const calendars = (calendarsData ?? []).map((c) => ({
    key: c.id,
    icon: React.createElement(CalendarOutlined),
    label: c.name,
  }));

  const onCalendarClick: MenuProps["onClick"] = (e) => {
    if (e.key != undefined) setActiveCalendar(e?.key);
  };

  return (
    <>
      <PrimaryHeader onCreateEvent={() => setIsModalOpen(true)} />

      <Layout className="min-h-screen bg-gray-50">
        <Sider width="25%">
          <Menu
            theme="dark"
            mode="inline"
            selectedKeys={[activeCalendar]}
            items={calendars ?? []}
            onClick={onCalendarClick}
          />

          <Button
            onClick={() => {
              localStorage.clear();
              router.push("/sign-in");
            }}
          >
            Logout
          </Button>
        </Sider>
        <Content className="p-8">
          {/* Dropdowns */}
          <div style={{ marginBottom: 10 }}>
            <select value={currentDate.month()} onChange={handleMonthChange}>
              {months.map((month, idx) => (
                <option key={month} value={idx}>
                  {month}
                </option>
              ))}
            </select>

            <select value={currentDate.year()} onChange={handleYearChange}>
              {years.map((year) => (
                <option key={year} value={year}>
                  {year}
                </option>
              ))}
            </select>
          </div>
          <Calendar<ExpandEvent>
            localizer={localizer}
            events={eventsData ?? []}
            startAccessor="start"
            endAccessor="end"
            style={{ height: 500 }}
            date={currentDate.toDate()}
            onNavigate={(date) => setCurrentDate(moment(date))}
            defaultView="month"
          />
        </Content>
      </Layout>

      <Modal
        title="Add Event"
        open={isModalOpen}
        onOk={handleOk}
        onCancel={() => setIsModalOpen(false)}
        okText="Save"
      >
        <Form
          layout="vertical"
          form={form}
          initialValues={{
            date: [dayjs(), dayjs()],
            recurrence: false,
            relative_weekday: 0,
            relative_week_number: 0,
          }}
        >
          <Form.Item
            name="name"
            label="Event Title"
            rules={[{ required: true }]}
          >
            <Input placeholder="e.g. Team Meeting" />
          </Form.Item>
          <Form.Item name="description" label="Description">
            <Input.TextArea rows={3} placeholder="Optional details" />
          </Form.Item>
          <Form.Item name="date" label="Date" rules={[{ required: true }]}>
            <RangePicker showTime className="w-full" />
          </Form.Item>
          <Form.Item
            name="recurrence"
            label="Recurring"
            valuePropName="checked"
          >
            <Checkbox>Recurrence</Checkbox>
          </Form.Item>

          {watch_recurrence && (
            <>
              <Form.Item
                name="freq"
                label="Frequency"
                rules={[{ required: true }]}
              >
                <Select
                  defaultValue="daily"
                  style={{ width: "100%" }}
                  options={[
                    { value: "daily", label: "Daily" },
                    { value: "weekly", label: "Weekly" },
                    { value: "monthly", label: "Monthly" },
                    { value: "yearly", label: "Yearly" },
                  ]}
                />
              </Form.Item>
            </>
          )}

          {useWatch("freq", form) == "monthly" ? (
            <>
              <Form.Item
                name="relative_weekday"
                label="Weekday Selection(Every week day)"
                rules={[{ required: true }]}
              >
                <Select
                  defaultValue={0}
                  style={{ width: "100%" }}
                  labelInValue
                  options={[
                    { value: 0, label: "Monday" },
                    { value: 1, label: "Tuesday" },
                    { value: 2, label: "Wednesday" },
                    { value: 3, label: "Thursday" },
                    { value: 4, label: "Friday" },
                    { value: 5, label: "Saturday" },
                    { value: 6, label: "Sunday" },
                  ]}
                />
              </Form.Item>

              <Form.Item
                name="relative_week_number"
                label="Relative week number(Every week day)"
              >
                <Select
                  defaultValue={0}
                  style={{ width: "100%" }}
                  options={[
                    {
                      value: 0,
                      label: `Every month's ${watch_relative_weekday}`,
                    },
                    {
                      value: 1,
                      label: `Every month's 1st ${watch_relative_weekday}`,
                    },
                    {
                      value: 2,
                      label: `Every month's 2nd ${watch_relative_weekday}`,
                    },
                    {
                      value: 3,
                      label: `Every month's 3rd ${watch_relative_weekday}`,
                    },
                    {
                      value: 4,
                      label: `Every month's last ${watch_relative_weekday}`,
                    },
                  ]}
                />
              </Form.Item>
            </>
          ) : (
            <>
              {watch_recurrence && (
                <Form.Item
                  name="interval"
                  label="Interval"
                  rules={[{ required: true, min: 1, max: 365 }]}
                  style={{ width: "100%" }}
                >
                  <Input
                    type="number"
                    step={1}
                    min={1}
                    max={365}
                    width={"100%"}
                    style={{ width: "100%" }}
                  />
                </Form.Item>
              )}
            </>
          )}

          <Form.Item name="recurrence_end_date" label="Recurrence End Date">
            <DatePicker style={{ width: "100%" }} />
          </Form.Item>
        </Form>
      </Modal>
    </>
  );
}
